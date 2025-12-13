import argparse
import copy
import typing

import edq.util.hash

import autograder.api.constants
import autograder.error

CSV_TO_LIST_DELIMITER: str = ','
MAP_KEY_VALUE_SEP: str = '='

class APIParam(object):
    def __init__(self,
            config_key, description,
            cli_flag = None,
            payload_key = None,
            required = True,
            cli_required = False,
            cli = True,
            value_type: typing.Type = str,
            clean = True, omit_empty = True,
            parser_options = {'action': 'store', 'type': str},
            parser_add_func = None,
            hash = False):
        if ((config_key is None) or (len(config_key.strip()) == 0)):
            raise autograder.error.APIError(None, "APIParam cannot have an empty key.")

        self.config_key = str(config_key)  # Key in the config dict.

        self.description = str(description)
        if ((description is None) or (self.description == '')):
            raise autograder.error.APIError(None, "APIParam cannot have an empty description.")

        if (cli_flag is None):
            cli_flag = config_key.replace('_', '-')

        self.cli_flag = cli_flag  # Flag to put on the CLI.

        if (payload_key is None):
            payload_key = config_key

        self.payload_key = payload_key  # Key to put in the autograder payload.

        self.required = required  # Required when calling the API.
        self.cli_required = cli_required  # Required on the CLI.
        self.cli = cli
        self.clean = clean
        self.value_type = value_type
        self.omit_empty = omit_empty
        self.parser_options = parser_options
        self.hash = hash

        # A full override of parser adding behavior.
        self.parser_add_func = parser_add_func

    def clean_value(self, value: typing.Union[typing.Any, None]) -> typing.Union[typing.Any, None]:
        """
        Return a clean version of the given value (according to this API param).
        An error will be raised if cleaning fails.
        Empty values will be returned as None.
        """

        if (not self.clean):
            return value

        if (value is None):
            return None

        if (issubclass(self.value_type, str)):
            value = str(value).strip()
            if (len(value) == 0):
                return None

            if (self.hash):
                value = edq.util.hash.sha256_hex(value)

        return value

    def optional(self) -> 'APIParam':
        """ Make a copy of this APIParam, mark the copy as optional, and return the copy. """

        new_param = copy.deepcopy(self)
        new_param.required = False
        return new_param

    def required(self) -> 'APIParam':
        """ Make a copy of this APIParam, mark the copy as required, and return the copy. """

        new_param = copy.deepcopy(self)
        new_param.required = True
        return new_param

class ArgumentMap(argparse.Action):
    def __call__(self, parser, namespace, raw_values, option_string = None):
        if (not hasattr(namespace, self.dest)):
            setattr(namespace, self.dest, {})

        allValues = getattr(namespace, self.dest)
        if (allValues is None):
            allValues = {}
            setattr(namespace, self.dest, allValues)

        for raw_value in raw_values:
            parts = raw_value.split(MAP_KEY_VALUE_SEP, 1)
            if (len(parts) != 2):
                raise ValueError((
                    "Argument map key/value pair ('%s') is missing a separator '%s'."
                    % (raw_value, MAP_KEY_VALUE_SEP)))

            allValues[parts[0].strip()] = parts[1].strip()

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

PARAM_ASSIGNMENT_ID = APIParam('assignment_id',
    'The ID of the assignment to make this request to.',
    required = True)

PARAM_COURSE_EMAIL_BCC = APIParam('bcc',
    ('A list of email addresses.'
    + ' Accepts course user references.'),
    required = False,
    parser_options = {'action': 'extend', 'type': _csv_to_list})

PARAM_COURSE_EMAIL_CC = APIParam('cc',
    ('A list of email addresses.'
    + ' Accepts course user references.'),
    required = False,
    parser_options = {'action': 'extend', 'type': _csv_to_list})

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
    parser_options = {'action': 'extend', 'type': _csv_to_list})

PARAM_COURSE_ID = APIParam('course_id',
    'The ID of the course to make this request to.',
    required = True)

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
    parser_options = {'action': 'extend', 'type': _csv_to_list})

PARAM_DRY_RUN = APIParam('dry_run',
    ('Do not commit/finalize the operation,'
    + ' just do all the steps and state what the result would look like.'),
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

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
    parser_options = {
        'action': 'store',
        'default': 'unknown',
        'choices': autograder.api.constants.COURSE_ROLES})

PARAM_FORCE = APIParam('force',
    'Force the operation, overwriting any existing resources.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_NEW_PASS = APIParam('new_pass',
    'The new password to set for the user that is the target of this request.',
    required = True, hash = True)

PARAM_OVERWRITE_RECORDS = APIParam('overwrite_records',
    ('Replace any existing records that match the current operation'
        + ' (e.g. re-do existing results).'),
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

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
    required = False, parser_options = {'action': 'store', 'type': int})

PARAM_QUERY_LIMIT = APIParam('limit',
    'The maximum number of records to return.',
    required = False, parser_options = {'action': 'store', 'type': int})

PARAM_QUERY_AFTER = APIParam('after',
    'If supplied, only return records after this timestamp.',
    required = False, parser_options = {'action': 'store', 'type': int})

PARAM_QUERY_BEFORE = APIParam('before',
    'If supplied, only return records before this timestamp.',
    required = False, parser_options = {'action': 'store', 'type': int})

PARAM_QUERY_SORT = APIParam('sort',
    'Sort the results. -1 for ascending, 0 for no sorting, 1 for descending.',
    required = False, parser_options = {'action': 'store', 'type': int})

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
    parser_options = {
        'metavar': (f"KEY{MAP_KEY_VALUE_SEP}VALUE"),
        'action': ArgumentMap,
        'nargs': '+',
    })

PARAM_REGRADE_CUTOFF = APIParam('regrade_cutoff',
    ('All submissions occurring before the cutoff time will be regraded.'
    + ' By default, the current time will be used.'
    + ' Time is milliseconds from the UNIX epoch'
    + ' (https://en.wikipedia.org/wiki/Unix_time).'),
    required = False, parser_options = {'action': 'store', 'type': int})

PARAM_SEND_EMAILS = APIParam('send_emails',
    'Send any emails.',
    required = True, cli = False)

PARAM_SERVER = APIParam('server',
    'The URL of the autograder server to communicate with.',
    required = True)

PARAM_SERVER_USER_REFERENCES = APIParam('target_users',
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
    required = False,
    parser_options = {'action': 'extend', 'type': _csv_to_list})

PARAM_SKIP_BUILD_IMAGES = APIParam('skip_build_images',
    'Skip building assignment Docker images.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_EMAILS = APIParam('skip_emails',
    'Skip sending any emails. Be aware that this may result in inaccessible information.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_INSERTS = APIParam('skip_inserts',
    'Skip inserts (default: False).',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_LMS_SYNC = APIParam('skip_lms_sync',
    'Skip syncing with the LMS.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_SOURCE_SYNC = APIParam('skip_source_sync',
    'Skip syncing (updating with) the course source.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_TASKS = APIParam('skip_tasks',
    'Skip starting course tasks.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

PARAM_SKIP_UPDATES = APIParam('skip_updates',
    'Skip updates (default: False).',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})

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
    parser_add_func = _submission_add_func)

PARAM_TARGET_EMAIL = APIParam('target_email',
    'The email of the user that is the target of this request.',
    required = True)

PARAM_TARGET_EMAIL_OR_SELF = APIParam('target_email',
    'The email of the user that is the target of this request (defaults to you).',
    required = False)

PARAM_TARGET_PASS = APIParam('target_pass',
    'The password of the user that is the target of this request.',
    required = True, hash = True)

PARAM_TARGET_SUBMISSION_OR_RECENT = APIParam('target_submission',
    'The ID of the submission (default to the most recent submission).',
    required = False)

PARAM_USER_EMAIL = APIParam('user',
    'The email of the user making this request.',
    payload_key = 'user-email',
    required = True)

PARAM_USER_PASS = APIParam('pass',
    'The password of the user making this request.',
    payload_key = 'user-pass',
    required = True, hash = True)

PARAM_WAIT_FOR_COMPLETION = APIParam('wait_for_completion',
    'Wait for the full analysis to complete before returning.',
    required = False,
    parser_options = {'action': 'store_true', 'default': False})
