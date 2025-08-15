import sys

import autograder.api.config

DESCRIPTION = "List your current configuration options."

def run(args):
    (config, sources) = autograder.api.config.get_tiered_config(
        cli_arguments = args,
        skip_keys = [
            'show_origin', 'verbose',
            autograder.api.config.CONFIG_PATHS_KEY, 'global_config_path',
        ],
        global_config_path = args.global_config_path
    )

    config_list = []
    for (key, value) in config.items():
        config_str = f"{key}\t{value}"
        if (args.show_origin):
            raw_source = sources.get(key)
            source_path = raw_source.split(autograder.api.config.CONFIG_TYPE_DELIMITER)[1]
            config_str += f"\t{source_path}"

        config_list.append(config_str)

    print("\n".join(config_list))
    return 0

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        skip_server = True)

    parser.add_argument("--show-origin", dest = 'show_origin',
        action = 'store_true', help = "Shows where each configuration's value was obtained from.")

    parser.add_argument("--global-config", dest = 'global_config_path',
        action = 'store', type = str, default = autograder.api.config.DEFAULT_GLOBAL_CONFIG_PATH,
        help = 'Path to the global configuration file (default: %(default)s).')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
