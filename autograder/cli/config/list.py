import sys

import autograder.api.config

DESCRIPTION = "List configurations."

def run(args):
    arguments = {
        "cli_arguments": args,
        "skip_keys": ['show_origin', 'verbose', autograder.api.config.CONFIG_PATHS_KEY],
        "show_sources": args.show_origin,
    }

    configs, sources  = autograder.api.config.get_tiered_config(**arguments)
    for config, cred in configs.items():
        config_str = ''
        if sources != None:
            raw_source = sources.get(config)
            source_path = raw_source.split("::")[1]
            config_str = config_str + source_path + "\t"

        config_str = config_str + f'{config}: {cred}'
        print(config_str)
    return 0

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        skip_server = True)

    parser.add_argument("--show-origin", dest = 'show_origin',
        action = 'store_true', help = 'Show origin of configs.')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
