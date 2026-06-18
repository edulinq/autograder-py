"""
Customize an argument parser for the autograder.
"""

import argparse
import typing

import edq.core.argparser
import edq.net.exchange
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
        ) -> argparse.ArgumentParser:
    """
    Get an argument parser specialized for autograder-py.
    """

    if (api_params is None):
        api_params = []

    config_options: typing.Dict[str, typing.Any] = {
        'config_filename': CONFIG_FILENAME,
        'legacy_config_filename': DEPRECATED_CONFIG_FILENAME,
        'cli_arg_config_map': {},
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

    # Add arguments according to the given API params.
    group = parser.add_argument_group('command-specific options')
    for api_param in api_params:
        api_param.add_to_parser(group)

    group = parser.add_argument_group('testing options')
    group.add_argument('--testing-mode', dest = 'testing_mode',
        action = 'store_true', default = False,
        help = 'Run as if a test is being run (default: %(default)s).')

    # Ensure that responses are cleaned as API responses.
    if (include_net):
        if (_set_exchanges_clean_func):
            edq.net.exchange._exchanges_clean_func = edq.util.reflection.get_qualified_name(autograder.util.net.clean_api_response)

    if (include_output_format):
        group = parser.add_argument_group('output formatting options')

        group.add_argument('--format', dest = 'output_format',
            action = 'store', type = str,
            default = lms.model.constants.OutputFormat.TEXT.value,
            choices = [choice.value for choice in lms.model.constants.OutputFormat],
            help = 'The format to display the output as (default: %(default)s).')

        group.add_argument('--include-extra-fields', dest = 'include_extra_fields',
            action = 'store_true', default = False,
            help = 'Include uncommon fields in results (default: %(default)s).')

        group.add_argument('--pretty-headers', dest = 'pretty_headers',
            action = 'store_true', default = False,
            help = 'When displaying headers, try to make them look "pretty" (default: %(default)s).')

        group.add_argument('--skip-headers', dest = 'skip_headers',
            action = 'store_true', default = False,
            help = 'Skip headers when outputting results, will not apply to all formats (default: %(default)s).')

    if (include_skip_rows):
        parser.add_argument('--skip-rows', dest = 'skip_rows',
            action = 'store', type = int, default = DEFAULT_SKIP_ROWS,
            help = 'The number of header rows to skip (default: %(default)s).')

    return parser
