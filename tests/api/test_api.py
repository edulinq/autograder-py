import glob
import json
import importlib
import os
import re

import tests.server.base

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
TEST_CASES_DIR = os.path.join(THIS_DIR, "testdata")
DATA_DIR = os.path.join(THIS_DIR, '..', "data")

REWRITE_TOKEN_ID = '<TOKEN_ID>'
REWRITE_TOKEN_CLEARTEXT = '<TOKEN_CLEARTEXT>'

SUBMISSION_ID_PATTERN = r'\b\d{10}\b'
SUBMISSION_ID_REPLACEMENT = '1234567890'

TIMESTAMP_PATTERN = r'\b\d{13}\b'
TIMESTAMP_REPLACEMENT = '1234567890123'

TIME_DELTA_PATTERN = r'(\d+h)?(\d+m)?(\d+\.)?(\d+[mun]?s)'
TIME_DELTA_REPLACEMENT = '<time-delta:1234567890123>'

TIME_MESSAGE_PATTERN = r'<timestamp:(-?\d+|nil)>'
TIME_MESSAGE_REPLACEMENT = '<timestamp:1234567890123>'

class APITest(tests.server.base.ServerBaseTest):
    """
    Test API calls by mocking a server.

    Note that the same test output is used by the server to respond to a request
    and the test to verify the output (making the equality assertion seem redundant).
    However, the autograder server will verify that the output is correct in it's own test suite.
    """

    def _get_test_info(self, path):
        return _get_api_test_info(path, self.get_base_arguments())

def _get_api_test_info(path, arguments):
    with open(path, 'r') as file:
        data = json.load(file)

    import_module_name = data.get('module', None)
    if (import_module_name is None):
        raise ValueError("Could not find API test module.")

    for key, value in data.get('arguments', {}).items():
        arguments[key] = value

    files = data.get('files', [])
    for i in range(len(files)):
        path = files[i]
        files[i] = tests.server.base.replace_path(path, tests.server.base.DATA_DIR_ID, DATA_DIR)

    is_error = data.get('error', False)
    read_write = data.get('read-write', False)

    output = data['output']

    output_modifier = clean_output_noop
    if ('output-modifier' in data):
        modifier_name = data['output-modifier']

        if (modifier_name not in globals()):
            raise ValueError("Could not find API output modifier function: '%s'." % (
                modifier_name))

        output_modifier = globals()[modifier_name]

    return import_module_name, arguments, files, output, is_error, read_write, output_modifier

def _discover_api_tests():
    for path in sorted(glob.glob(os.path.join(TEST_CASES_DIR, "**", "*.json"), recursive = True)):
        try:
            _add_api_test(path)
        except Exception as ex:
            raise ValueError("Failed to parse test case '%s'." % (path)) from ex

def _add_api_test(path):
    test_name = os.path.splitext(os.path.basename(path))[0]
    setattr(APITest, 'test_api__' + test_name, _get_api_test_method(path))

def _get_api_test_method(path):
    def __method(self):
        parts = self._get_test_info(path)
        (module_name, arguments, files, expected, is_error, read_write, output_modifier) = parts

        api_module = importlib.import_module(module_name)

        try:
            actual = api_module.send(arguments, files = files)
        except Exception as ex:
            if (not is_error):
                raise ex

            python_message = expected.get('python-message', "")
            self.assertEqual(python_message, str(ex))

            code = expected.get('code', None)
            self.assertEqual(code, ex.code)

            return

        if (is_error):
            self.fail("Test case does not raise an error when one was expected: '%s'." % (path))
            return

        actual = output_modifier(actual)

        self.assertDictEqual(actual, expected)

    return __method

def clean_output_noop(output):
    return output

def clean_output_timestamps(output):
    # Convert the output to JSON so we can do a simple find/replace for all timestamps-like things.
    text_output = json.dumps(output)

    text_output = re.sub(TIMESTAMP_PATTERN, TIMESTAMP_REPLACEMENT, text_output)
    text_output = re.sub(TIME_DELTA_PATTERN, TIME_DELTA_REPLACEMENT, text_output)
    text_output = re.sub(TIME_MESSAGE_PATTERN, TIME_MESSAGE_REPLACEMENT, text_output)

    return json.loads(text_output)

def clean_output_timestamps_and_submission_ids(output):
    output = clean_output_timestamps(output)

    # Convert the output to JSON so we can do a simple find/replace for all timestamps-like things.
    text_output = json.dumps(output)

    text_output = re.sub(SUBMISSION_ID_PATTERN, SUBMISSION_ID_REPLACEMENT, text_output)

    return json.loads(text_output)

def clean_token(output):
    output['token-id'] = REWRITE_TOKEN_ID
    output['token-cleartext'] = REWRITE_TOKEN_CLEARTEXT

    return output

def clean_output_logs(output):
    record_set_values = {
        'timestamp': 0,
    }

    attribute_set_values = {
        'path': '/some/path/course.json',
        'unix_socket': '/tmp/autograder.sock',
        'port': 8080,
    }

    if (output.get('results') is None):
        return output

    for record in output['results']:
        for (key, value) in record_set_values.items():
            record[key] = value

        if ('attributes' not in record):
            continue

        for (key, value) in attribute_set_values.items():
            record['attributes'][key] = value

    # Sort the output for consistency.
    output['results'] = sorted(output['results'], key = lambda record: record['message'])

    return output

def fake_stats_cpu(output):
    """
    Because of the variable and fine-grained level of stats,
    the entire output must be faked.
    """

    return {
        "results": [
            {
                "timestamp": 100,
                "type": "cpu-usage",
                "value": 1
            },
            {
                "timestamp": 200,
                "type": "cpu-usage",
                "value": 2
            },
            {
                "timestamp": 300,
                "type": "cpu-usage",
                "value": 3
            }
        ],
    }

def fake_stats_grading_time(output):
    """
    Because of the variable and fine-grained level of stats,
    the entire output must be faked.
    """

    return {
        "results": [
            {
                "timestamp": 100,
                "type": "grading-time",
                "value": 100,
                "attributes": {
                    "assignment": "hw0",
                    "course": "course101",
                    "user": "server-admin@test.edulinq.org"
                }
            },
            {
                "timestamp": 100,
                "type": "grading-time",
                "value": 100,
                "attributes": {
                    "assignment": "hw0",
                    "course": "course101",
                    "user": "server-admin@test.edulinq.org"
                }
            }
        ]
    }

# flake8: noqa: E501
def fake_system_stacks(output):
    """
    Fake consistent stack traces.
    """

    return {
        "stacks": [
            {
                "name": "goroutine 1",
                "status": "chan receive, 3 minutes",
                "records": [
                    {
                        "call": "github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock(0xc0003422b0, {0xe4a5fb?, 0x0?})",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/api/server/server.go",
                        "line": 63,
                        "pointer": "+0x265"
                    },
                    {
                        "call": "github.com/edulinq/autograder/internal/procedures/server.RunAndBlock.RunAndBlockFull.func1(0xc000091e78, {0xe4a5fb, 0xe}, 0xe0?)",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/procedures/server/start.go",
                        "line": 112,
                        "pointer": "+0x115"
                    },
                    {
                        "call": "github.com/edulinq/autograder/internal/procedures/server.RunAndBlockFull(...)",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/procedures/server/start.go",
                        "line": 117,
                        "pointer": ""
                    },
                    {
                        "call": "github.com/edulinq/autograder/internal/procedures/server.RunAndBlock({0xe4a5fb?, 0x0?})",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/procedures/server/start.go",
                        "line": 95,
                        "pointer": "+0x2b"
                    },
                    {
                        "call": "main.main()",
                        "file": "/home/eriq/code/autograder/autograder-server/cmd/server/main.go",
                        "line": 23,
                        "pointer": "+0xf6"
                    }
                ]
            },
            {
                "name": "goroutine 7",
                "status": "chan receive, 3 minutes",
                "records": [
                    {
                        "call": "github.com/edulinq/autograder/internal/common.removeStaleLocks()",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/common/lockmanager.go",
                        "line": 95,
                        "pointer": "+0x54"
                    },
                    {
                        "call": "created by github.com/edulinq/autograder/internal/common.init.0 in goroutine 1",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/common/lockmanager.go",
                        "line": 28,
                        "pointer": "+0x4c"
                    }
                ]
            },
            {
                "name": "goroutine 21",
                "status": "sleep, 2 minutes",
                "records": [
                    {
                        "call": "time.Sleep(0x1bf08eb000)",
                        "file": "/usr/lib/go/src/runtime/time.go",
                        "line": 300,
                        "pointer": "+0xf2"
                    },
                    {
                        "call": "github.com/edulinq/autograder/internal/tasks.runTasks()",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/tasks/core.go",
                        "line": 57,
                        "pointer": "+0x6f"
                    },
                    {
                        "call": "created by github.com/edulinq/autograder/internal/tasks.Start in goroutine 1",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/tasks/core.go",
                        "line": 26,
                        "pointer": "+0x7f"
                    }
                ]
            },
            {
                "name": "goroutine 25",
                "status": "syscall, 3 minutes",
                "records": [
                    {
                        "call": "os/signal.signal_recv()",
                        "file": "/usr/lib/go/src/runtime/sigqueue.go",
                        "line": 152,
                        "pointer": "+0x29"
                    },
                    {
                        "call": "os/signal.loop()",
                        "file": "/usr/lib/go/src/os/signal/signal_unix.go",
                        "line": 23,
                        "pointer": "+0x13"
                    },
                    {
                        "call": "created by os/signal.Notify.func1.1 in goroutine 1",
                        "file": "/usr/lib/go/src/os/signal/signal.go",
                        "line": 151,
                        "pointer": "+0x1f"
                    }
                ]
            },
            {
                "name": "goroutine 26",
                "status": "chan receive, 3 minutes",
                "records": [
                    {
                        "call": "github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock.func4()",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/api/server/server.go",
                        "line": 56,
                        "pointer": "+0x25"
                    },
                    {
                        "call": "created by github.com/edulinq/autograder/internal/api/server.(*APIServer).RunAndBlock in goroutine 1",
                        "file": "/home/eriq/code/autograder/autograder-server/internal/api/server/server.go",
                        "line": 55,
                        "pointer": "+0x23f"
                    }
                ]
            },
            {
                "name": "goroutine 99",
                "status": "IO wait",
                "records": [
                    {
                        "call": "internal/poll.runtime_pollWait(0x790e13448ca0, 0x72)",
                        "file": "/usr/lib/go/src/runtime/netpoll.go",
                        "line": 351,
                        "pointer": "+0x85"
                    },
                    {
                        "call": "internal/poll.(*pollDesc).wait(0xc000182380?, 0xc000162131?, 0x0)",
                        "file": "/usr/lib/go/src/internal/poll/fd_poll_runtime.go",
                        "line": 84,
                        "pointer": "+0x27"
                    },
                    {
                        "call": "internal/poll.(*pollDesc).waitRead(...)",
                        "file": "/usr/lib/go/src/internal/poll/fd_poll_runtime.go",
                        "line": 89,
                        "pointer": ""
                    },
                    {
                        "call": "internal/poll.(*FD).Read(0xc000182380, {0xc000162131, 0x1, 0x1})",
                        "file": "/usr/lib/go/src/internal/poll/fd_unix.go",
                        "line": 165,
                        "pointer": "+0x27a"
                    },
                    {
                        "call": "net.(*netFD).Read(0xc000182380, {0xc000162131?, 0x0?, 0x0?})",
                        "file": "/usr/lib/go/src/net/fd_posix.go",
                        "line": 55,
                        "pointer": "+0x25"
                    },
                    {
                        "call": "net.(*conn).Read(0xc000452060, {0xc000162131?, 0x0?, 0x0?})",
                        "file": "/usr/lib/go/src/net/net.go",
                        "line": 189,
                        "pointer": "+0x45"
                    },
                    {
                        "call": "net/http.(*connReader).backgroundRead(0xc000162120)",
                        "file": "/usr/lib/go/src/net/http/server.go",
                        "line": 690,
                        "pointer": "+0x37"
                    },
                    {
                        "call": "created by net/http.(*connReader).startBackgroundRead in goroutine 98",
                        "file": "/usr/lib/go/src/net/http/server.go",
                        "line": 686,
                        "pointer": "+0xb6"
                    }
                ]
            }
        ]
    }

_discover_api_tests()
