import argparse
import copy
import typing

import edq.util.hash
import edq.util.parse

import autograder.api.constants
import autograder.error

CSV_TO_LIST_DELIMITER: str = ','
MAP_KEY_VALUE_SEP: str = '='

DEFAULT_CLI_ACTIONS: typing.Dict[typing.Type, str] = {
    bool: 'store_true',
    float: 'store',
    int: 'store',
    str: 'store',
}
""" Map value types to default CLI actions. """

class APIParam:
    """
    A definition for a parameter to the autograder API.
    This class also contains information for representing these parameters in
    config (dicts) and on the CLI (argparse options).
    """

    def __init__(self,
            config_key: str,
            description: str,
            api_key: typing.Union[str, None] = None,
            cli_flag: typing.Union[str, None] = None,
            api_required: bool = True,
            cli_required: bool = False,
            cli: bool = True,
            value_type: typing.Type = str,
            cli_type: typing.Union[typing.Any, None] = None,
            skip_clean: bool = False,
            hash_value: bool = False,
            omit_empty: bool = True,
            cli_action: typing.Union[typing.Any, None] = None,
            cli_default_value: typing.Any = None,
            cli_show_default: bool = True,
            cli_extra_options: typing.Union[typing.Dict[str, typing.Any], None] = None,
            cli_add_func: typing.Union[typing.Callable, None] = None,
            **kwargs: typing.Any) -> None:
        if (len(config_key.strip()) == 0):
            raise autograder.error.APIError(None, "APIParam cannot have an empty key.")

        self.config_key: str = config_key
        """
        The main key/label used to reference this parameter.
        Will be used in config dicts.
        """

        if (len(description) == 0):
            raise autograder.error.APIError(None, "APIParam cannot have an empty description.")

        self.description: str = description
        """ A description used for this parameter. """

        if (api_key is None):
            api_key = config_key.replace('_', '-')

        self.api_key: str = api_key
        """ The key in the API request payload for this parameter. """

        if (cli_flag is None):
            cli_flag = config_key.replace('_', '-')

        self.cli_flag: str = cli_flag
        """ The flag used on the CLI for this parameter. """

        self.api_required: bool = api_required
        """ If this parameter is required when calling the API. """

        self.cli_required: bool = cli_required
        """ If this parameter is required on the CLI. """

        self.cli: bool = cli
        """ If this parameter should be included on the CLI. """

        self.value_type: typing.Type = value_type
        """ The type that a clean value from this parameter should be. """

        if (cli_type is None):
            cli_type = self.value_type

        self.cli_type: typing.Any = cli_type
        """
        The type of value that will be looked for on the CLI.
        Defaults to the same as `self.value_type`.

        Note that this value will be used as the `type` argument to `argparse.ArgumentParser.add_argument()`.
        """

        self.skip_clean: bool = skip_clean
        """ Skip any cleaning steps for this parameter's value. """

        self.hash_value: bool = hash_value
        """ Hash the value during the cleaning processes (typically used for passwords). """

        self.omit_empty: bool = omit_empty
        """ Do not include this parameter in the API payload if its value is empty. """

        if (cli_action is None):
            # Choose action based on the value's type.
            cli_action = DEFAULT_CLI_ACTIONS.get(self.value_type, None)
            if (cli_action is None):
                raise ValueError(f"Unknown action for value type '{self.value_type}'.")

        self.cli_action: typing.Any = cli_action
        """ The value that value will be used as the `action` argument to `argparse.ArgumentParser.add_argument()`. """

        self.cli_default_value: typing.Any = cli_default_value
        """ The default value for the CLI argument. """

        self.cli_show_default: bool = cli_show_default
        """ Show the default value (in CLI's help) for a non-required param. """

        if (cli_extra_options is None):
            cli_extra_options = {}

        self.cli_extra_options: typing.Dict[str, typing.Any] = cli_extra_options
        """
        Additional options to pass (as kwargs) to `argparse.ArgumentParser.add_argument()`.
        These should not conflict with the options set using the direct members.
        """

        self.cli_add_func: typing.Union[typing.Callable, None] = cli_add_func
        """ A function that can be used to override the standard behavior in add_to_parser(). """

    def clean_value(self, value: typing.Union[typing.Any, None]) -> typing.Union[typing.Any, None]:
        """
        Return a clean version of the given value (according to this API param).
        An error will be raised if cleaning fails.
        Empty values will be returned as None.
        """

        if (self.skip_clean):
            return value

        if (value is None):
            return None

        if (issubclass(self.value_type, bool)):
            return edq.util.parse.boolean(value)

        if (issubclass(self.value_type, str)):
            value = str(value).strip()
            if (len(value) == 0):
                return None

            if (self.hash_value):
                value = edq.util.hash.sha256_hex(value)

        return value

    def optional(self) -> 'APIParam':
        """ Make a copy of this APIParam, mark the copy as optional, and return the copy. """

        new_param = copy.deepcopy(self)
        new_param.api_required = False
        new_param.cli_required = False
        return new_param

    def required(self) -> 'APIParam':
        """ Make a copy of this APIParam, mark the copy as required, and return the copy. """

        new_param = copy.deepcopy(self)
        new_param.api_required = True
        new_param.cli_required = True
        return new_param

    def add_to_parser(self, parser: argparse.ArgumentParser) -> None:
        """
        Add this API parameter to the given parser.
        If this parameter is not supposed to be represented as a CLI argument, it will not be added.
        """

        if (not self.cli):
            return

        # Check if there is a specialized function for this param.
        if (self.cli_add_func is not None):
            self.cli_add_func(parser, self)
            return

        kwargs = {
            'dest': self.config_key,
            'action': self.cli_action,
            'help': self.description,
        }

        if (not self.cli_action in {'store_true', 'store_false'}):
            kwargs['type'] = self.cli_type

        if (self.cli_required):
            kwargs['required'] = True
        else:
            kwargs['required'] = False
            kwargs['default'] = self.cli_default_value

            if (self.cli_show_default):
                kwargs['help'] += ' (default: %(default)s)'

        kwargs.update(self.cli_extra_options)

        parser.add_argument(f'--{self.cli_flag}', **kwargs)

class ArgumentMap(argparse.Action):
    """ An argparse Action for key/value pairs separated with MAP_KEY_VALUE_SEP. """

    def __call__(self, parser, namespace, raw_values, option_string = None):
        if (not hasattr(namespace, self.dest)):
            setattr(namespace, self.dest, {})

        all_values = getattr(namespace, self.dest)
        if (all_values is None):
            all_values = {}
            setattr(namespace, self.dest, all_values)

        for raw_value in raw_values:
            parts = raw_value.split(MAP_KEY_VALUE_SEP, 1)
            if (len(parts) != 2):
                raise ValueError(f"Argument map key/value pair ('{raw_value}') is missing a separator '{MAP_KEY_VALUE_SEP}'.")

            all_values[parts[0].strip()] = parts[1].strip()

def _submission_add_func(parser, param):
    parser.add_argument('submissions', metavar = 'SUBMISSION',
        action = 'store', type = str, nargs = '+',
        help = param.description)

# This is used as an argparse argument type.
# See: https://docs.python.org/3/library/argparse.html#type
# This converts a csv string and returns a list of strings,
# e.g. --to email1@gmail.com,email2@gmail.com -> ["email1@gmail.com", "email2@gmail.com"].
def _csv_to_list(arg):
    if arg == "" or arg is None:
        raise ValueError('Parameter argument cannot be empty.')

    return [part.strip() for part in arg.split(CSV_TO_LIST_DELIMITER)]

# Common API params.

PARAM_COURSE = APIParam(
    'course',
    'The ID of the course to make this request to.',
    api_key = 'course-id',
    cli_show_default = False,
)

PARAM_SERVER = APIParam(
    'server',
    'The URL of the autograder server to communicate with.',
)

PARAM_TARGET_USERS = APIParam(
    'target_users',
    ('A list of server user references.'
    + ' Server user references may be specified in eight ways:'
    + ' 1) Email address of the requested user,'
    + ' 2) "*" to request all users in the server,'
    + ' 3) "<server role>" (e.g., user, creator)'
    + ' to request all users with that server role,'
    + ' 4) "<course id>::<course role>" (e.g., course101::student)'
    + ' to request all users in the target course with that course role,'
    + ' 5) "*::<course role>" (e.g., *::student)'
    + ' to request all users with that course role in any course,'
    + ' 6) "<course id>::*" to request all users in the target course,'
    + ' 7) "*::*" to request all users enrolled in at least one course,'
    + ' and 8) any of the previous options preceded by a minus sign'
    + ' (e.g., "-alice@test.edulinq.org", "-user", "-*::student")'
    + ' to exclude that user or group from the request.'
    + ' Default: All users in the server.'),
    api_required = False,
    value_type = list,
    cli_action = 'extend',
    cli_type = _csv_to_list,
    cli_show_default = False,
)

PARAM_USER_EMAIL = APIParam(
    'user',
    'The email of the user making this request.',
    api_key = 'user-email',
    cli_show_default = False,
)

PARAM_USER_PASS = APIParam(
    'pass',
    'The password of the user making this request.',
    api_key = 'user-pass',
    hash_value = True,
    cli_show_default = False,
)

''' TEST
PARAM_ASSIGNMENT_ID = APIParam('assignment_id',
    'The ID of the assignment to make this request to.',
    required = True)

PARAM_COURSE_EMAIL_BCC = APIParam('bcc',
    ('A list of email addresses.'
    + ' Accepts course user references.'),
    required = False,
    cli_options = {'action': 'extend', 'type': _csv_to_list})

PARAM_COURSE_EMAIL_CC = APIParam('cc',
    ('A list of email addresses.'
    + ' Accepts course user references.'),
    required = False,
    cli_options = {'action': 'extend', 'type': _csv_to_list})

PARAM_COURSE_EMAIL_TO = APIParam('to',
    ('A list of email addresses.'
    + ' Accepts course user references.'
    + ' Course user references may be specified in four ways:'
    + ' 1) Email address of the requested user,'
    + ' 2) "*" to request all users in the course,'
    + ' 3) "<course role>" (e.g., student, grader)'
    + ' to request all course users with that role,'
    + ' and 4) any of the previous options preceded by a minus sign'
    + ' (e.g., "-alice@test.edulinq.org", "-student")'
    + ' to exclude that user or role from the request.'),
    required = False,
    cli_options = {'action': 'extend', 'type': _csv_to_list})

PARAM_COURSE_SOURCE = APIParam('source',
    'The source to use for the course.',
    required = False)

PARAM_COURSE_USER_REFERENCES = APIParam('target_users',
    ('A list of course user references.'
    + ' Course user references may be specified in four ways:'
    + ' 1) Email address of the requested user,'
    + ' 2) "*" to request all users in the course,'
    + ' 3) "<course role>" (e.g., student, grader)'
    + ' to request all course users with that role,'
    + ' and 4) any of the previous options preceded by a minus sign'
    + ' (e.g., "-alice@test.edulinq.org", "-student")'
    + ' to exclude that user or role from the request.'
    + ' Default: All users in the course.'),
    required = False,
    cli_options = {'action': 'extend', 'type': _csv_to_list})

PARAM_DRY_RUN = APIParam('dry_run',
    ('Do not commit/finalize the operation,'
    + ' just do all the steps and state what the result would look like.'),
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_EMAIL_BODY = APIParam('body',
    'The email body.',
    required = False)

PARAM_EMAIL_HTML = APIParam('html',
    'Indicates the email body contains HTML.',
    required = False)

PARAM_EMAIL_SUBJECT = APIParam('subject',
    'The email subject.',
    required = True)

PARAM_FILTER_ROLE = APIParam('filter_role',
    'Only show results from users with this role (all roles if unknown (default)).',
    required = False,
    cli_options = {
        'action': 'store',
        'default': 'unknown',
        'choices': autograder.api.constants.COURSE_ROLES})

PARAM_FORCE = APIParam('force',
    'Force the operation, overwriting any existing resources.',
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_NEW_PASS = APIParam('new_pass',
    'The new password to set for the user that is the target of this request.',
    required = True, hash_value = True)

PARAM_OVERWRITE_RECORDS = APIParam('overwrite_records',
    ('Replace any existing records that match the current operation'
        + ' (e.g. re-do existing results).'),
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_PROXY_EMAIL = APIParam('proxy_email',
    ('The email of the user the request is pretending to be made under'
    + ' (the submission will be made on behalf of this user).'),
    required = True)

PARAM_PROXY_TIME = APIParam('proxy_time',
    ('The proxy timestamp that will be applied to the request.'
    + ' By default, the earlier time between now and'
    + ' one minute before the due date will be used.'
    + ' Use this option to manually set the proxy time.'
    + ' Timestamps are milliseconds from the UNIX epoch'
    + ' (https://en.wikipedia.org/wiki/Unix_time).'),
    required = False, cli_options = {'action': 'store', 'type': int})

PARAM_QUERY_LIMIT = APIParam('limit',
    'The maximum number of records to return.',
    required = False, cli_options = {'action': 'store', 'type': int})

PARAM_QUERY_AFTER = APIParam('after',
    'If supplied, only return records after this timestamp.',
    required = False, cli_options = {'action': 'store', 'type': int})

PARAM_QUERY_BEFORE = APIParam('before',
    'If supplied, only return records before this timestamp.',
    required = False, cli_options = {'action': 'store', 'type': int})

PARAM_QUERY_SORT = APIParam('sort',
    'Sort the results. -1 for ascending, 0 for no sorting, 1 for descending.',
    required = False, cli_options = {'action': 'store', 'type': int})

PARAM_QUERY_TARGET_ASSIGNMENT = APIParam('target_assignment',
    'If supplied, only return records for this assignment.',
    required = False)

PARAM_QUERY_TARGET_COURSE = APIParam('target_course',
    'If supplied, only return records for this course.',
    required = False)

PARAM_QUERY_TARGET_EMAIL = APIParam('target_email',
    'If supplied, only return records for this user.',
    required = False)

PARAM_QUERY_TYPE = APIParam('type',
    'The type of metric to query for.',
    required = True)

PARAM_QUERY_WHERE = APIParam('where',
    'Only includes records with a patching key/value pair.',
    required = False,
    cli_options = {
        'metavar': (f"KEY{MAP_KEY_VALUE_SEP}VALUE"),
        'action': ArgumentMap,
        'nargs': '+',
    })

PARAM_REGRADE_CUTOFF = APIParam('regrade_cutoff',
    ('All submissions occurring before the cutoff time will be regraded.'
    + ' By default, the current time will be used.'
    + ' Time is milliseconds from the UNIX epoch'
    + ' (https://en.wikipedia.org/wiki/Unix_time).'),
    required = False, cli_options = {'action': 'store', 'type': int})

# TEST - We can make this a CLI param, but we want it to default false and be `--skip-emails`.
PARAM_SEND_EMAILS = APIParam('send_emails',
    'Send any emails.',
    required = True, cli = False)

def add_skip_emails_argument(parser):
    parser.add_argument('--skip-emails', dest = 'skip-emails',
        action = 'store_true', default = False,
        help = 'Skip sending any emails. Be aware that this may result in inaccessible'
        + ' information (default: %(default)s).')

PARAM_SKIP_BUILD_IMAGES = APIParam('skip_build_images',
    'Skip building assignment Docker images.',
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_EMAILS = APIParam('skip_emails',
    'Skip sending any emails. Be aware that this may result in inaccessible information.',
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_INSERTS = APIParam('skip_inserts',
    'Skip inserts (default: False).',
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_LMS_SYNC = APIParam('skip_lms_sync',
    'Skip syncing with the LMS.',
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_SOURCE_SYNC = APIParam('skip_source_sync',
    'Skip syncing (updating with) the course source.',
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_TASKS = APIParam('skip_tasks',
    'Skip starting course tasks.',
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_UPDATES = APIParam('skip_updates',
    'Skip updates (default: False).',
    required = False,
    cli_options = {'action': 'store_true', 'default': False})

PARAM_SUBMISSION_MESSAGE = APIParam('message',
        'An optional message to attach to the submission.',
        required = False)

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
    required = True,
    cli_add_func = _submission_add_func)

PARAM_TARGET_EMAIL = APIParam('target_email',
    'The email of the user that is the target of this request.',
    required = True)

PARAM_TARGET_EMAIL_OR_SELF = APIParam('target_email',
    'The email of the user that is the target of this request (defaults to you).',
    required = False)

PARAM_TARGET_PASS = APIParam('target_pass',
    'The password of the user that is the target of this request.',
    required = True, hash_value = True)

PARAM_TARGET_SUBMISSION_OR_RECENT = APIParam('target_submission',
    'The ID of the submission (default to the most recent submission).',
    required = False)

PARAM_WAIT_FOR_COMPLETION = APIParam('wait_for_completion',
    'Wait for the full analysis to complete before returning.',
    required = False,
    cli_options = {'action': 'store_true', 'default': False})
'''
