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
import autograder.util.net

CONFIG_FILENAME: str = 'autograder.json'
DEPRECATED_CONFIG_FILENAME: str = 'config.json'

DEFAULT_SKIP_ROWS: int = 0

_set_exchanges_clean_func: bool = True  # pylint: disable=invalid-name

def get_parser(
        description: str,
        api_params: typing.List[autograder.api.config.APIParam],
        include_output_format: bool = False,
        include_net: bool = True,
        include_skip_rows: bool = False,
        ) -> argparse.ArgumentParser:
    """
    Get an argument parser specialized for Autograder-Py.
    """

    config_options = {
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
        # Only include CLI params.
        if (not api_param.cli):
            continue

        # Check if there is a specialized function for this param.
        if (api_param.parser_add_func is not None):
            api_param.parser_add_func(parser, api_param)
            continue

        parser.add_argument(f'--{api_param.cli_flag}', dest = api_param.config_key,
            required = api_param.cli_required,
            help = api_param.description,
            **api_param.parser_options)

    return parser
