import argparse
import os
import typing

import edq.procedure.verify_exchanges
import edq.testing.run

import autograder.testing.server
import autograder.testing.serverrunner

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_PACKAGE_DIR: str = os.path.join(THIS_DIR, '..')
ROOT_DIR: str = os.path.join(ROOT_PACKAGE_DIR, '..')

def generate(args: typing.Union[argparse.Namespace, typing.Dict[str, typing.Any]]) -> int:
    """
    Generate HTTP test data by
    setting an exchange path, pointing to a live autograder server, and running all tests.
    The arguments may come directly from the parser for autograder.cli.testing.generate-test-data.
    """

    if (not isinstance(args, dict)):
        args = vars(args)

    args.update(args.get('_config', {}))

    server_runner = autograder.testing.serverrunner.ServerRunner(**args)
    server_runner.start()

    # Configure tests.
    autograder.testing.server.ServerTest.skip_test_exchanges_base = True
    autograder.testing.server.ServerTest.override_server_url = server_runner.server

    # Run the tests (which generate the data).
    test_args = {
        'test_dirs': [ROOT_PACKAGE_DIR],
        'fail_fast': args.get('fail_fast', False),
        'pattern': args.get('pattern', None),
        'discover_top_level_dir': ROOT_DIR,
    }
    failure_count = int(edq.testing.run.run(test_args))

    server_runner.stop()

    return failure_count

def verify(args: typing.Union[argparse.Namespace, typing.Dict[str, typing.Any]]) -> int:
    """
    Verify that test data matches data returned by the autograder server.
    The arguments may come directly from the parser for autograder.cli.testing.verify-test-data.
    """

    if (not isinstance(args, dict)):
        args = vars(args)

    args.update(args.get('_config', {}))

    test_data_dir = args.get('test_data_dir', None)
    if (test_data_dir is None):
        raise ValueError("No test data dir was providded.")

    server_runner = autograder.testing.serverrunner.ServerRunner(**args)
    server_runner.start()

    failure_count = int(edq.procedure.verify_exchanges.run([test_data_dir], server_runner.server, fail_fast = args.get('fail_fast', False)))

    server_runner.stop()

    return failure_count
