import argparse
import json
import os
import sys

import platformdirs

import autograder.api.constants
import autograder.error
import autograder.util.hash

DEFAULT_CONFIG_FILENAME = 'config.json'
DEFAULT_USER_CONFIG_PATH = platformdirs.user_config_dir('autograder.json')

CONFIG_PATHS_KEY = 'config_paths'

class APIParam(object):
    def __init__(self, key, description,
            config_key = None, required = True, cli_param = True,
            parser_options = {'action': 'store', 'type': str},
            parser_add_func = None,
            hash = False):
        self.key = str(key)
        if ((key is None) or (self.key == '')):
            raise autograder.error.APIError(None, "APIParam cannot have an empty key.")

        self.description = str(description)
        if ((description is None) or (self.description == '')):
            raise autograder.error.APIError(None, "APIParam cannot have an empty description.")

        self.config_key = config_key
        if (self.config_key is None):
            self.config_key = key

        self.required = required
        self.cli_param = cli_param
        self.parser_options = parser_options
        self.hash = hash

        # A full override of parser adding behavior.
        self.parser_add_func = parser_add_func

def parse_api_config(config, params,
        additional_required_keys = ['server'],
        additional_optional_keys = ['verbose'],
        exit_on_error = False):
    """
    Given a tiered config and api parameters,
    return a dict that can be directly sierialized and sent to the autograder.
    Any hashed params that are not empty will be hashed.
    If |exit_on_error| is true sys.exit() will be called on an error,
    otherwise an error will be raised on an error.
    Any keys in |additional_*_keys| will be returned in a second dict.

    Returns: (<values derived from params>, <additional values>)
    """

    try:
        return _parse_api_config(config, params,
                additional_required_keys, additional_optional_keys)
    except autograder.error.APIError as ex:
        if (exit_on_error):
            print("ERROR: " + ex.args[0], file = sys.stderr)
            autograder.error.exit_from_error(1)

        raise ex

def _parse_api_config(config, params, additional_required_keys, additional_optional_keys):
    data = {}
    extra = {}

    for param in params:
        if (param.config_key not in config):
            if (param.required):
                raise autograder.error.APIError(None,
                    f"Required parameter '{param.config_key}' not set.")

            continue

        value = config[param.config_key]
        if (param.hash and (value != '')):
            value = autograder.util.hash.sha256_hex(value)

        data[param.key] = value

    for key in additional_required_keys:
        if (key not in config):
            raise autograder.error.APIError(None, f"Required parameter '{key}' not set.")

        extra[key] = config[key]

    for key in additional_optional_keys:
        if (key not in config):
            continue

        extra[key] = config[key]

    return data, extra

def get_tiered_config(cli_arguments, skip_keys = [CONFIG_PATHS_KEY], show_sources = False):
    """
    Get all the tiered configuration options (from files and CLI).
    If |show_sources| is True, then an addition dict will be returned that shows each key,
    and where that key came from.
    """

    config = {}
    sources = {}

    if (isinstance(cli_arguments, argparse.Namespace)):
        cli_arguments = vars(cli_arguments)

    # Check the current directory config.
    if (os.path.isfile(DEFAULT_CONFIG_FILENAME)):
        with open(DEFAULT_CONFIG_FILENAME, 'r') as file:
            for key, value in json.load(file).items():
                config[key] = value
                sources[key] = "<default config file>::" + DEFAULT_CONFIG_FILENAME

    # Check the user config file.
    if (os.path.isfile(DEFAULT_USER_CONFIG_PATH)):
        with open(DEFAULT_USER_CONFIG_PATH, 'r') as file:
            for key, value in json.load(file).items():
                config[key] = value
                sources[key] = "<user config file>::" + DEFAULT_USER_CONFIG_PATH

    # Check the config files specified on the command-line.
    config_paths = cli_arguments.get(CONFIG_PATHS_KEY, [])
    if (config_paths is not None):
        for path in config_paths:
            with open(path, 'r') as file:
                for key, value in json.load(file).items():
                    config[key] = value
                    sources[key] = "<cli config file>::" + path

    # Finally, any command-line options.
    for (key, value) in cli_arguments.items():
        if (key in skip_keys):
            continue

        if ((value is None) or (value == '')):
            continue

        config[key] = value
        sources[key] = "<cli argument>"

    if (show_sources):
        return config, sources

    return config

def get_argument_parser(
        description = 'Send an API request to the autograder.',
        params = [],
        include_assignment = True):
    """
    Create an argparse parser that has all the standard options for API requests.
    """

    parser = argparse.ArgumentParser(
        description = description,
        formatter_class = argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--config', dest = CONFIG_PATHS_KEY,
        action = 'append', type = str,
        help = 'A JSON config file with your submission/authentication details.'
            + " Can be specified multiple times with later values overriding earlier ones."
            + " Config values can be specified in multiple places"
            + " (with later values overriding earlier values):"
            + " First './%s'," % (DEFAULT_CONFIG_FILENAME)
            + " then '%s'," % (DEFAULT_USER_CONFIG_PATH)
            + " now any files specified using --config in the order they were specified,"
            + " and finally any variables specified directly on the command line (like --user).")

    parser.add_argument('--server', dest = 'server',
        action = 'store', type = str, default = None,
        help = 'The URL of the server to submit to (default: %(default)s).')

    parser.add_argument('-v', '--verbose', dest = 'verbose',
        action = 'store_true', default = False,
        help = 'Output detailed information about the API request and response'
            + " (default: %(default)s).")

    for param in params:
        if (not param.cli_param):
            continue

        if (param.parser_add_func is not None):
            param.parser_add_func(parser, param)
        else:
            parser.add_argument(f'--{param.config_key}', dest = param.config_key,
                help = param.description,
                **param.parser_options)

    return parser

def _submission_add_func(parser, param):
    parser.add_argument('submissions', metavar = 'SUBMISSION',
        action = 'store', type = str, nargs = '+',
        help = param.description)

# Common API params.

PARAM_ASSIGNMENT_ID = APIParam('assignment-id',
    'The ID of the assignment to make this request to.',
    config_key = 'assignment', required = True)

PARAM_COURSE_ID = APIParam('course-id',
    'The ID of the course to make this request to.',
    config_key = 'course', required = True)

PARAM_COURSE_SOURCE = APIParam('source',
    'The source to use for the course.',
    required = False)

PARAM_DRY_RUN = APIParam('dry-run',
    ('Do not commit/finalize the operation,'
    + ' just do all the steps and state what the result would look like.'),
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_FILTER_ROLE = APIParam('filter-role',
    'Only show results from users with this role (all roles if unknown (default)).',
    required = False,
    parser_options = {'action': 'store', 'default': 'unknown',
        'choices': autograder.api.constants.COURSE_ROLES})

PARAM_FORCE = APIParam('force',
    'Force the operation, overwriting and existing resources.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_NEW_PASS = APIParam('new-pass',
    'The new password to set for the user that is the target of this request.',
    required = True, hash = True)

PARAM_QUERY_LIMIT = APIParam('limit',
    'The maximum number of records to return.',
    required = False, parser_options = {'action': 'store', 'type': int})

PARAM_QUERY_AFTER = APIParam('after',
    'If supplied, only return records after this timestamp.',
    required = False)

PARAM_QUERY_BEFORE = APIParam('before',
    'If supplied, only return records before this timestamp.',
    required = False)

PARAM_QUERY_SORT = APIParam('sort',
    'Sort the results. -1 for ascending, 0 for no sorting, 1 for descending.',
    required = False, parser_options = {'action': 'store', 'type': int})

PARAM_QUERY_TARGET_COURSE = APIParam('target-course',
    'If supplied, only return records for this course.',
    required = False)

PARAM_QUERY_TARGET_ASSIGNMENT = APIParam('target-assignment',
    'If supplied, only return records for this assignment.',
    required = False)

PARAM_QUERY_TARGET_EMAIL = APIParam('target-email',
    'If supplied, only return records for this user.',
    required = False)

PARAM_SEND_EMAILS = APIParam('send-emails',
    'Send any emails.',
    required = True, cli_param = False)

PARAM_SKIP_BUILD_IMAGES = APIParam('skip-build-images',
    'Skip building assignment Docker images.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_EMAILS = APIParam('skip-emails',
    'Skip sending any emails. Be aware that this may result in inaccessible information.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_INSERTS = APIParam('skip-inserts',
    'Skip inserts (default: False).',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_LMS_SYNC = APIParam('skip-lms-sync',
    'Skip syncing with the LMS.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_SOURCE_SYNC = APIParam('skip-source-sync',
    'Skip syncing (updating with) the course sourse.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_TASKS = APIParam('skip-tasks',
    'Skip starting course tasks.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_UPDATES = APIParam('skip-updates',
'Skip updates (default: False).',
required = False,
parser_options = {'action': 'store_true', 'default': False})

PARAM_SUBMISSION_SPECS = APIParam('submissions',
    ('A list of submission specifications to analyze.'
    + ' Submissions may span courses and assignments.'
    + ' Submissions may be specified in three ways:'
    + ' 1) "<course id>::<assignment id>::<user email>::<submission short id>"'
    + ' for a specific submission,'
    + ' 2) "<course id>::<assignment id>::<user email>"'
    + ' for the given user\'s most recent submission to the given assignment,'
    + ' and 3) "<course id>::<assignment id>"'
    + ' for the most recent submission for all students.'),
    config_key = 'submissions', required = True,
    parser_add_func = _submission_add_func)

PARAM_TARGET_EMAIL = APIParam('target-email',
    'The email of the user that is the target of this request.',
    required = True)

PARAM_TARGET_EMAIL_OR_SELF = APIParam('target-email',
    'The email of the user that is the target of this request (defaults to you).',
    required = False)

PARAM_TARGET_PASS = APIParam('target-pass',
    'The password of the user that is the target of this request.',
    required = True, hash = True)

PARAM_TARGET_SUBMISSION_OR_RECENT = APIParam('target-submission',
    'The ID of the submission (default to the most recent submission).',
    required = False)

PARAM_USER_EMAIL = APIParam('user-email',
    'The email of the user making this request.',
    config_key = 'user', required = True)

PARAM_USER_PASS = APIParam('user-pass',
    'The password of the user making this request.',
    config_key = 'pass', required = True, hash = True)

PARAM_WAIT_FOR_COMPLETION = APIParam('wait-for-completion',
    'Wait for the full analysis to complete before returning.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})
