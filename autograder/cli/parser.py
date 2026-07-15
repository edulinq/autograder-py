"""
Customize an argument parser for the autograder.
"""

import argparse
import typing

import edq.config.settings
import edq.config.source
import edq.core.argparser
import edq.net.settings
import edq.util.reflection
import lms.model.constants

import autograder
import autograder.api.common
import autograder.model.config
import autograder.util.net

CONFIG_FILENAME: str = 'autograder.json'
LOCAL_CONFIG_FILENAME: str = 'config.json'
ENV_CONFIG_PREFIX: str = 'AG__'
DEFAULT_ENCRYPTION_KEY: str = 'LynxGrader'

DEFAULT_SKIP_ROWS: int = 0

_set_exchanges_clean_response_func: bool = True  # pylint: disable=invalid-name

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

    # Set config options.
    edq.config.settings.set_config_filename(CONFIG_FILENAME)
    edq.config.settings.set_application_config_class(autograder.model.config.Config)
    edq.config.settings.set_env_prefix(ENV_CONFIG_PREFIX)
    edq.config.settings.set_default_encryption_key(DEFAULT_ENCRYPTION_KEY)
    edq.config.settings.set_load_order([
        edq.config.source.LocalSpec(filename = LOCAL_CONFIG_FILENAME),
        edq.config.source.GlobalSpec(),
        edq.config.source.ProjectSpec(),
        edq.config.source.ENVSpec(),
        edq.config.source.CLIFileSpec(),
        edq.config.source.CLIImplicitSpec(),
        edq.config.source.CLIExplicitSpec(),
    ])

    parser = edq.core.argparser.get_default_parser(
            description,
            version = f"v{autograder.__version__}",
            include_net = include_net,
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
        if (_set_exchanges_clean_response_func):
            edq.net.settings.set_exchanges_clean_response_func(edq.util.reflection.get_qualified_name(autograder.util.net.clean_api_response))

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
