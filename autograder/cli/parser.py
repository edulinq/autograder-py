"""
Customize an argument parser for the autograder.
"""

import argparse
import typing

import edq.core.argparser
import edq.util.net
import edq.util.reflection
import lms.model.constants

import autograder
import autograder.api.common
import autograder.util.net

CONFIG_FILENAME: str = 'autograder.json'
DEPRECATED_CONFIG_FILENAME: str = 'config.json'

DEFAULT_SKIP_ROWS: int = 0

_set_exchanges_clean_func: bool = True  # pylint: disable=invalid-name

def _post_parse(
        parser: argparse.ArgumentParser,
        args: argparse.Namespace,
        extra_state: typing.Dict[str, typing.Any]) -> None:
    """ Called after argument parsing. """

    if (args.testing_mode):
        autograder.api.common.set_testing_source_info()

def get_parser(
        description: str,
        api_params: typing.Union[typing.List[autograder.api.config.APIParam], None] = None,
        include_output_format: bool = False,
        include_net: bool = True,
        include_skip_rows: bool = False,
        include_submission_files: bool = False,
        include_new_action_course_role: typing.Union[str, None] = None,
        include_new_action_email: typing.Union[str, None] = None,
        include_new_action_lms_id: typing.Union[str, None] = None,
        include_new_action_name: typing.Union[str, None] = None,
        ) -> argparse.ArgumentParser:
    """
    Get an argument parser specialized for autograder-py.

    The `include_new_action_*` arguments expect either None (if they should not be included),
    or the name of the action to include in the help messages.
    """

    if (api_params is None):
        api_params = []

    config_options: typing.Dict[str, typing.Any] = {
        'config_filename': CONFIG_FILENAME,
        'legacy_config_filename': DEPRECATED_CONFIG_FILENAME,
        'cli_arg_config_map': dict(),
    }

    # Ensure that all relevant CLI params are copied over to the config.
    for api_param in api_params:
        config_options['cli_arg_config_map'][api_param.config_key] = api_param.config_key

    parser = edq.core.argparser.get_default_parser(
            description,
            version = f"v{autograder.__version__}",
            include_net = include_net,
            config_options = config_options,
    )

    parser.register_callbacks('autograder-py', None, _post_parse)

    parser.add_argument('--testing-mode', dest = 'testing_mode',
        action = 'store_true', default = False,
        help = 'Run as if a test is being run (default: %(default)s).')

    # Ensure that responses are cleaned as API responses.
    if (include_net):
        if (_set_exchanges_clean_func):
            edq.util.net._exchanges_clean_func = edq.util.reflection.get_qualified_name(autograder.util.net.clean_api_response)

    if (include_output_format):
        parser.add_argument('--format', dest = 'output_format',
            action = 'store', type = str,
            default = lms.model.constants.OUTPUT_FORMAT_TEXT, choices = lms.model.constants.OUTPUT_FORMATS,
            help = 'The format to display the output as (default: %(default)s).')

        parser.add_argument('--skip-headers', dest = 'skip_headers',
            action = 'store_true', default = False,
            help = 'Skip headers when outputting results, will not apply to all formats (default: %(default)s).')

        parser.add_argument('--pretty-headers', dest = 'pretty_headers',
            action = 'store_true', default = False,
            help = 'When displaying headers, try to make them look "pretty" (default: %(default)s).')

        parser.add_argument('--include-extra-fields', dest = 'include_extra_fields',
            action = 'store_true', default = False,
            help = 'Include uncommon fields in results (default: %(default)s).')

    if (include_skip_rows):
        parser.add_argument('--skip-rows', dest = 'skip_rows',
            action = 'store', type = int, default = DEFAULT_SKIP_ROWS,
            help = 'The number of header rows to skip (default: %(default)s).')

    # Add arguments according to the given API params.
    for api_param in api_params:
        api_param.add_to_parser(parser)

    if (include_submission_files):
        parser.add_argument('files', metavar = 'FILE',
            action = 'store', type = str, nargs = '+',
            help = 'The path to your submission file(s).')

    if (include_new_action_course_role is not None):
        parser.add_argument('--new-course-role', dest = 'new-course-role',
            action = 'store', type = str, default = 'student',
            choices = autograder.api.constants.COURSE_ROLES,
            help = f'The course role of the user to {include_new_action_course_role} (default: %(default)s).')

    if (include_new_action_email is not None):
        parser.add_argument('--new-email', dest = 'new-email',
            action = 'store', type = str, required = True,
            help = f'The email of the user to {include_new_action_email}.')

    if (include_new_action_lms_id is not None):
        parser.add_argument('--new-lms-id', dest = 'new-lms-id',
            action = 'store', type = str, default = '',
            help = f'The lms id of the user to {include_new_action_lms_id}.')

    if (include_new_action_name is not None):
        parser.add_argument('--new-name', dest = 'new-name',
            action = 'store', type = str, default = '',
            help = f'The name of the user to {include_new_action_name}.')

    return parser
