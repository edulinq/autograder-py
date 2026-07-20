import argparse
import copy
import typing

import edq.util.hash
import edq.util.parse
import edq.util.time

import autograder.api.constants
import autograder.model.log
import autograder.model.stats
import autograder.model.user
import autograder.error
import autograder.filespec
import autograder.util.parse

CSV_TO_LIST_DELIMITER: str = ','
MAP_KEY_VALUE_SEP: str = '='

DEFAULT_CLI_ACTIONS: typing.Dict[typing.Type, str] = {
    bool: 'store_true',
    edq.util.time.Timestamp: 'store',
    float: 'store',
    int: 'store',
    str: 'store',
}
""" Map value types to default CLI actions. """

@typing.runtime_checkable
class CLIAddFunction(typing.Protocol):
    """ A function for manually adding APIParams to a parser. """

    def __call__(self, parser: typing.Union[argparse.ArgumentParser, argparse._ArgumentGroup], param: 'APIParam') -> None:
        """
        Add the given APIParam to the parser.
        """

class APIParam:
    """
    A definition for a parameter to the autograder API.
    This class also contains information for representing these parameters in
    config (dicts), on the CLI (argparse options), and in the payload of autograder requests.
    """

    def __init__(self,
            config_key: str,
            description: str,
            alt_config_key: typing.Union[str, None] = None,
            api_key: typing.Union[str, None] = None,
            cli_flag: typing.Union[str, None] = None,
            api: bool = True,
            api_required: typing.Union[bool, None] = None,  # Default to the value of `api`.
            cli: bool = True,
            cli_required: typing.Union[bool, None] = None,  # Default to false.
            value_type: typing.Type = str,
            cli_type: typing.Union[typing.Any, None] = None,
            skip_clean: bool = False,
            hash_value: bool = False,
            omit_empty: bool = True,
            cli_action: typing.Union[typing.Any, None] = None,
            cli_default_value: typing.Any = None,
            cli_show_default: typing.Union[bool, None] = None,
            cli_extra_options: typing.Union[typing.Dict[str, typing.Any], None] = None,
            cli_add_func: typing.Union[CLIAddFunction, None] = None,
            **kwargs: typing.Any) -> None:
        if (len(config_key.strip()) == 0):
            raise autograder.error.APIError(None, "APIParam cannot have an empty key.")

        self.config_key: str = config_key
        """
        The main key/label used to reference this parameter.
        Will be used in the application config and config dicts.
        """

        if (len(description) == 0):
            raise autograder.error.APIError(None, "APIParam cannot have an empty description.")

        self.description: str = description
        """ A description used for this parameter. """

        self.alt_config_key: typing.Union[str, None] = alt_config_key
        """
        An alternative config key that the value could be found under when reading a config file.
        A value found under this key will always be stored under self.config_key.
        """

        if (api_key is None):
            api_key = config_key.replace('_', '-')

        self.api_key: str = api_key
        """ The key in the API request payload for this parameter. """

        if (cli_flag is None):
            cli_flag = config_key.replace('_', '-')

        self.cli_flag: str = cli_flag
        """ The flag used on the CLI for this parameter. """

        self.api: bool = api
        """ If this parameter should be included on the API payload. """

        if (api_required is None):
            api_required = api

        self.api_required: bool = api_required
        """ If this parameter is required when calling the API. """

        self.cli: bool = cli
        """ If this parameter should be included on the CLI. """

        if (cli_required is None):
            cli_required = False

        self.cli_required: bool = cli_required
        """ If this parameter is required on the CLI. """

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

        self.cli_default_value: typing.Any = cli_default_value
        """ The default value for the CLI argument. """

        if (cli_show_default is None):
            # Usually we will want to show the default value,
            # but boolean flags don't make much sense to show defaults with.
            cli_show_default = (value_type != bool)

        self.cli_show_default: bool = cli_show_default
        """ Show the default value (in CLI's help) for a non-required param. """

        if (cli_extra_options is None):
            cli_extra_options = {}

        self.cli_extra_options: typing.Dict[str, typing.Any] = cli_extra_options
        """
        Additional options to pass (as kwargs) to `argparse.ArgumentParser.add_argument()`.
        These should not conflict with the options set using the direct members.
        """

        self.cli_add_func: typing.Union[CLIAddFunction, None] = cli_add_func
        """ A function that can be used to override the standard behavior in add_to_parser(). """

        if (self.cli and (self.cli_add_func is None) and (cli_action is None)):
            # Choose action based on the value's type.
            cli_action = DEFAULT_CLI_ACTIONS.get(self.value_type, None)
            if (cli_action is None):
                raise ValueError(f"Unknown action for value type '{self.value_type}'.")

        self.cli_action: typing.Any = cli_action
        """ The value that value will be used as the `action` argument to `argparse.ArgumentParser.add_argument()`. """

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

        if (issubclass(self.value_type, edq.util.time.Timestamp)):
            return edq.util.time.Timestamp.guess(value)

        if (issubclass(self.value_type, bool)):
            return edq.util.parse.boolean(value)

        if (issubclass(self.value_type, int)):
            return int(value)

        if (issubclass(self.value_type, list)):
            return autograder.util.parse.string_list(value)

        if (issubclass(self.value_type, str)):
            value = str(value).strip()
            if (len(value) == 0):
                return None

            if (self.hash_value):
                value = edq.util.hash.sha256_hex(value)

        if (issubclass(self.value_type, autograder.filespec.FileSpec)):
            return autograder.filespec.parse(value)

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

    def add_to_parser(self, parser: typing.Union[argparse.ArgumentParser, argparse._ArgumentGroup]) -> None:
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

        if (self.cli_action not in {'store_true', 'store_false'}):
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

    def __call__(self, parser, namespace, raw_values, option_string = None):  # type: ignore[no-untyped-def]
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

def _cli_add_func_submission_files(parser: typing.Union[argparse.ArgumentParser, argparse._ArgumentGroup], param: APIParam) -> None:
    parser.add_argument('files', metavar = 'FILE',
        action = 'extend', type = str, nargs = '+',
        help = param.description)

def _cli_add_func_submission_specs(parser: typing.Union[argparse.ArgumentParser, argparse._ArgumentGroup], param: APIParam) -> None:
    parser.add_argument('submission_specs', metavar = 'SUBMISSION',
        action = 'extend', type = str, nargs = '+',
        help = param.description)

def _cli_add_func_upsert_zip(parser: typing.Union[argparse.ArgumentParser, argparse._ArgumentGroup], param: APIParam) -> None:
    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = param.description)

# This is used as an argparse argument type.
# See: https://docs.python.org/3/library/argparse.html#type
# This converts a csv string and returns a list of strings,
# e.g. --to email1@gmail.com,email2@gmail.com -> ["email1@gmail.com", "email2@gmail.com"].
# This will strip each compnent.
def _csv_to_list(raw_argument: typing.Union[None, str]) -> typing.List[str]:
    if (raw_argument is None):
        raise ValueError('Parameter argument cannot be None.')

    raw_argument = raw_argument.strip()
    if (len(raw_argument) == 0):
        raise ValueError('Parameter argument cannot be empty.')

    return [part.strip() for part in raw_argument.split(CSV_TO_LIST_DELIMITER)]

# Common API params.

PARAM_ALLOW_LATE = APIParam(
    'allow_late',
    'Allow this submission to be graded, even if it is late.',
    value_type = bool,
    cli_default_value = False,
)

PARAM_ASSIGNMENT = APIParam(
    'assignment',
    'The ID of the assignment to make this request to.',
    api_key = 'assignment-id',
    cli_show_default = False,
)

PARAM_COURSE = APIParam(
    'course',
    'The ID of the course to make this request to.',
    api_key = 'course-id',
    cli_show_default = False,
)

PARAM_COURSE_USER_REFERENCES = APIParam(
    'target_users',
    ('A list of course user references.'
    + ' Course user references may be specified in four ways:'
    + ' 1) Email address of the requested user,'
    + ' 2) "*" to request all users in the course,'
    + ' 3) "<course role>" (e.g., student, grader) to request all course users with that role,'
    + ' and 4) any of the previous options preceded by a minus sign (e.g., "-alice@test.edulinq.org", "-student")'
    + ' to exclude that user or role from the request.'
    + ' Default: All users in the course.'),
    api_required = False,
    value_type = list,
    cli_action = 'extend',
    cli_type = _csv_to_list,
    cli_show_default = False,
)

PARAM_DRY_RUN = APIParam(
    'dry_run',
    'Do not commit/finalize the operation, just do all the steps and state what the result would look like.',
    api_required = False,
    value_type = bool,
    cli_default_value = False,
)

PARAM_EMAIL_BODY = APIParam(
    'body',
    'The email body.',
    api_required = False,
)

PARAM_EMAIL_COURSE_BCC = APIParam(
    'bcc',
    'A list of email addresses. Accepts course user references.',
    api_required = False,
    value_type = list,
    cli_action = 'extend',
    cli_type = _csv_to_list,
    cli_show_default = False,
)

PARAM_EMAIL_COURSE_CC = APIParam(
    'cc',
    'A list of email addresses. Accepts course user references.',
    api_required = False,
    value_type = list,
    cli_action = 'extend',
    cli_type = _csv_to_list,
    cli_show_default = False,
)

PARAM_EMAIL_COURSE_TO = APIParam(
    'to',
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
    api_required = False,
    value_type = list,
    cli_action = 'extend',
    cli_type = _csv_to_list,
    cli_show_default = False,
)

PARAM_EMAIL_HTML = APIParam(
    'email_html',
    'Indicates the email body contains HTML.',
    api_key = 'html',
    cli_flag = 'html',
    api_required = False,
    value_type = bool,
    cli_default_value = False,
)

PARAM_EMAIL_SUBJECT = APIParam(
    'subject',
    'The email subject.',
    cli_required = True,
)

PARAM_FILESPEC_PART_PATH = APIParam(
    'filespec_path',
    'The path the filespec points to.',
    api = False,
    cli_required = True,
    cli_flag = 'path',
    cli_default_value = '',
    cli_show_default = False,
)

PARAM_FILESPEC_PART_REFERENCE = APIParam(
    'filespec_reference',
    'The reference (e.g., git commit/branch) of the filespec.',
    api = False,
    cli_flag = 'reference',
    cli_default_value = '',
    cli_show_default = False,
)

PARAM_FILESPEC_PART_TOKEN = APIParam(
    'filespec_token',
    'The token for filespec authentication.',
    api = False,
    cli_flag = 'token',
    cli_default_value = '',
    cli_show_default = False,
)

PARAM_FILESPEC_PART_TYPE = APIParam(
    'filespec_type',
    'The type of filespec.',
    api = False,
    cli_required = True,
    cli_flag = 'type',
    cli_default_value = '',
    cli_show_default = False,
)

PARAM_FILESPEC_PART_USERNAME = APIParam(
    'filespec_username',
    'The username for filespec authentication.',
    api = False,
    cli_flag = 'username',
    cli_default_value = '',
    cli_show_default = False,
)

PARAM_FORCE_COMPUTE = APIParam(
    'force_compute',
    'Force the server to compute the result, ignoring any existing cache.',
    api_required = False,
    value_type = bool,
    cli_default_value = False,
)

PARAM_NAME = APIParam(
    'name',
    'An optional name to use.',
    api_required = False,
)

PARAM_NEW_PASS = APIParam(
    'new_pass',
    'The new password.',
    hash_value = True,
    cli_required = True,
)

PARAM_NEW_USER_COURSE = APIParam(
    'new_course',
    'An optional course to enroll the new user in',
    api = False,
    cli_default_value = '',
    cli_show_default = False,
)

PARAM_NEW_USER_COURSE_ROLE = APIParam(
    'new_course_role',
    'The course role for the new user.',
    api = False,
    cli_default_value = autograder.model.user.CourseRole.STUDENT.value,
    cli_extra_options = {'choices': [role.value for role in autograder.model.user.CourseRole]},
)

PARAM_NEW_USER_EMAIL = APIParam(
    'new_email',
    'The email for the new user.',
    api = False,
    cli_required = True,
)

PARAM_NEW_USER_NAME = APIParam(
    'new_name',
    'The name for the new user.',
    api = False,
    cli_default_value = '',
    cli_show_default = False,
)

PARAM_NEW_USER_PASS = APIParam(
    'new_pass',
    'The password for the new user (random if not supplied).',
    api = False,
    cli_default_value = '',
    cli_show_default = False,
)

PARAM_NEW_USER_LMS_ID = APIParam(
    'new_lms_id',
    'The LMS ID for the new user.',
    api = False,
    cli_default_value = '',
    cli_show_default = False,
)

PARAM_NEW_USER_SERVER_ROLE = APIParam(
    'new_role',
    'The server role for the new user.',
    api = False,
    cli_default_value = autograder.model.user.ServerRole.USER.value,
    cli_extra_options = {'choices': [role.value for role in autograder.model.user.ServerRole]},
)

PARAM_OVERWRITE_RECORDS = APIParam(
    'overwrite_records',
    'Replace any existing records that match the current operation (e.g. re-do existing results).',
    value_type = bool,
    cli_default_value = False,
)

PARAM_OUT_DIR = APIParam(
    'out_dir',
    'A directory to write output in.',
    api = False,
    cli_default_value = '.',
)

PARAM_PROXY_EMAIL = APIParam(
    'proxy_email',
    'The email of the user the request is pretending to be made under (the submission will be made on behalf of this user).',
    cli_required = True,
)

PARAM_PROXY_TIME = APIParam(
    'proxy_time',
    ('The proxy timestamp that will be applied to the request.'
    + ' By default, the earlier time between now and'
    + ' one minute before the due date will be used.'
    + ' Use this option to manually set the proxy time.'
    + ' Timestamps are milliseconds from the UNIX epoch'
    + ' (https://en.wikipedia.org/wiki/Unix_time).'),
    value_type = edq.util.time.Timestamp,
    cli_type = str,
    api_required = False,
)

PARAM_QUERY_AFTER = APIParam(
    'query_after',
    'If supplied, only return records after this timestamp.',
    api_key = 'after',
    cli_flag = 'after',
    value_type = edq.util.time.Timestamp,
    api_required = False,
)

PARAM_QUERY_BEFORE = APIParam(
    'query_before',
    'If supplied, only return records before this timestamp.',
    api_key = 'before',
    cli_flag = 'before',
    value_type = edq.util.time.Timestamp,
    api_required = False,
)

PARAM_QUERY_LIMIT = APIParam(
    'limit',
    'The maximum number of records to return.',
    api_key = 'limit',
    cli_flag = 'limit',
    value_type = int,
    api_required = False,
)

PARAM_QUERY_LOG_LEVEL = APIParam(
    'query_level',
    'The minimum level of log records to return.',
    api_key = 'level',
    cli_flag = 'level',
    api_required = False,
    cli_default_value = 'INFO',
    cli_extra_options = {'choices': autograder.model.log.LOG_LEVEL_TEXT_TO_INT.keys()}
)

PARAM_QUERY_METRIC_TYPE = APIParam(
    'query_metric_type',
    'The type of metric to query for. See: https://github.com/edulinq/autograder-server/blob/main/internal/stats/metrics.go#L29',
    api_key = 'type',
    cli_flag = 'metric-type',
    cli_required = True,
    cli_extra_options = {'choices': autograder.model.stats.METRIC_TYPES}
)

PARAM_QUERY_PAST = APIParam(
    'query_past',
    'If supplied, only return log records in this duration (using "h", "m", or "s" suffixes) (e.g., "24h", "10m", or "1h10m10s").',
    api_key = 'past',
    cli_flag = 'past',
    api_required = False,
)

PARAM_QUERY_SORT = APIParam(
    'query_sort',
    'Sort the results. -1 for ascending, 0 for no sorting, 1 for descending.',
    api_key = 'sort',
    cli_flag = 'sort',
    value_type = int,
    api_required = False,
)

PARAM_QUERY_TARGET_ASSIGNMENT = APIParam(
    'query_target_assignment',
    'If supplied, only return records for this assignment.',
    api_key = 'target-assignment',
    cli_flag = 'target-assignment',
    api_required = False,
    cli_show_default = False,
)

PARAM_QUERY_TARGET_COURSE = APIParam(
    'query_target_course',
    'If supplied, only return records for this course.',
    api_key = 'target-course',
    cli_flag = 'target-course',
    api_required = False,
    cli_show_default = False,
)

PARAM_QUERY_TARGET_EMAIL = APIParam(
    'query_target_email',
    'If supplied, only return records for this user.',
    api_key = 'target-email',
    cli_flag = 'target-email',
    api_required = False,
    cli_show_default = False,
)

PARAM_QUERY_USE_TESTING_DATA = APIParam(
    'query_use_testing_data',
    'Query from hard-coded testing data (instead of real data).',
    api_key = 'use-testing-data',
    value_type = bool,
    api_required = False,
    cli = False,
)

PARAM_QUERY_WHERE = APIParam(
    'query_where',
    'Only includes records with a patching key/value pair.',
    api_key = 'where',
    cli_flag = 'where',
    api_required = False,
    value_type = dict,
    cli_action = ArgumentMap,
    cli_extra_options = {
        'metavar': (f"KEY{MAP_KEY_VALUE_SEP}VALUE"),
        'nargs': '+',
    },
)

PARAM_RAW_COURSE_USERS = APIParam(
    'raw_course_users',
    'Raw course users to operate on.',
    value_type = list,
    cli = False,
    skip_clean = True,
)

PARAM_RAW_SERVER_USERS = APIParam(
    'raw_server_users',
    'Raw server users to operate on.',
    value_type = list,
    api_key = 'raw-users',
    cli = False,
    skip_clean = True,
)

PARAM_REGRADE_CUTOFF = APIParam(
    'regrade_cutoff',
    ('All submissions occurring before the cutoff time will be regraded.'
    + ' By default, the current time will be used.'
    + ' Time is milliseconds from the UNIX epoch'
    + ' (https://en.wikipedia.org/wiki/Unix_time).'),
    value_type = int,
    api_required = False,
)

PARAM_SEND_EMAILS = APIParam(
    'send_emails',
    'Send any relevant emails to users affected by this operation (e.g., a user being enrolled in a course).',
    value_type = bool,
    cli_default_value = False,
)

PARAM_SERVER = APIParam(
    'server',
    'The URL of the autograder server to communicate with.',
    cli_show_default = False,
)

PARAM_SKIP_BUILD_IMAGES = APIParam(
    'skip_build_images',
    'Skip building assignment Docker images.',
    value_type = bool,
    cli_default_value = False,
)

PARAM_SKIP_EMAILS = APIParam(
    'skip_emails',
    'Skip sending any emails.',
    value_type = bool,
    cli_default_value = False,
)

PARAM_SKIP_INSERTS = APIParam(
    'skip_inserts',
    'Skip insert operations.',
    value_type = bool,
    cli_default_value = False,
)

PARAM_SKIP_LMS_SYNC = APIParam(
    'skip_lms_sync',
    'Skip syncing with the LMS.',
    value_type = bool,
    cli_default_value = False,
)

PARAM_SKIP_SOURCE_SYNC = APIParam(
    'skip_source_sync',
    'Skip syncing (updating with) the course source.',
    value_type = bool,
    cli_default_value = False,
)

PARAM_SKIP_TEMPLATE_FILES = APIParam(
    'skip_template_files',
    'Skip fetching assignment template files.',
    value_type = bool,
    cli_default_value = False,
)

PARAM_SKIP_UPDATES = APIParam(
    'skip_updates',
    'Skip update operations.',
    value_type = bool,
    cli_default_value = False,
)

PARAM_SUBMISSION_MESSAGE = APIParam(
    'message',
    'An optional message to attach to the submission.',
    api_required = False,
)

PARAM_SUBMISSION_FILES = APIParam(
    'files',
    'The path to your submission file(s).',
    value_type = list,
    api = False,
    cli_add_func = _cli_add_func_submission_files,
)

PARAM_SUBMISSION_SPECS = APIParam(
    'submission_specs',
    ('A list of submission specifications to analyze.'
    + ' Submissions may span courses and assignments.'
    + ' Submissions may be specified in three ways:'
    + ' 1) "<course id>::<assignment id>::<user email>::<submission short id> for a specific submission,'
    + ' 2) "<course id>::<assignment id>::<user email> for the given user\'s most recent submission to the given assignment,'
    + ' and 3) "<course id>::<assignment id> for the most recent submission for all students.'),
    api_key = 'submissions',
    cli_flag = 'submissions',
    value_type = list,
    cli_add_func = _cli_add_func_submission_specs,
)

PARAM_TARGET_ASSIGNMENTS = APIParam(
    'target_assignments',
    ('A list of assignment IDs to target.'
    + ' Default: All assignments in the course.'),
    api_required = False,
    value_type = list,
    cli_action = 'extend',
    cli_type = _csv_to_list,
    cli_show_default = False,
)

PARAM_TARGET_EMAIL = APIParam(
    'target_email',
    'The email of the user that is the target of this request.',
)

PARAM_TARGET_EMAIL_OR_SELF = APIParam(
    'target_email',
    'The email of the user that is the target of this request (defaults to you).',
    api_required = False,
)

PARAM_TARGET_USER_OR_SELF = APIParam(
    'target_user',
    'The user that is the target of this request (defaults to you).',
    api_required = False,
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

PARAM_TARGET_SUBMISSION_OR_RECENT = APIParam(
    'target_submission',
    'The ID of the submission (default to the most recent submission).',
    api_required = False,
)

PARAM_TOKEN_ID = APIParam(
    'token_id',
    'The id of the token to target.',
    cli_required = True,
)

PARAM_UPSERT_FILESPEC = APIParam(
    'filespec',
    'A filespec pointing to a course to upload.',
    value_type = autograder.filespec.FileSpec,
    cli = False,
)

PARAM_UPSERT_ZIP = APIParam(
    'path',
    ('The path to your course material.'
    + ' Either a zip file (with .zip extension) or directory (that will get zipped).'),
    value_type = str,
    api = False,
    cli_add_func = _cli_add_func_upsert_zip,
)

PARAM_USER_EMAIL = APIParam(
    'user',
    'The email of the user making this request.',
    alt_config_key = 'auth_user',
    api_key = 'user-email',
    cli_flag = 'user',
    cli_show_default = False,
)

PARAM_USER_PASS = APIParam(
    'pass',
    'The password of the user making this request.',
    alt_config_key = 'auth_pass',
    api_key = 'user-pass',
    cli_flag = 'pass',
    hash_value = True,
    cli_show_default = False,
)

PARAM_WAIT_FOR_COMPLETION = APIParam(
    'wait_for_completion',
    'Wait for the full job to complete before returning.',
    value_type = bool,
    cli_default_value = False,
)
