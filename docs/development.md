# Development

## Testing

This project has two main types of tests:
standard unit tests and server tests.

There is not much to say about the standard unit tests.
They are made using Python's `unittest` library.

The server test are much more involved.
These tests will mock an [Autograder API server](https://github.com/edulinq/autograder-server)
to send requests to.
Server tests come in two flavors:
API tests (which compare the direct output of API calls)
and CLI tests (which compare the output (typically stdout) of CLI executables).

### Running Tests

All tests can be run using the [run_tests.py](../run_tests.py) script:
```sh
./run_tests.py
```

This script also accept an argument that is a Python regular expression.
Only tests that match the regular expression will be run.
For example, to only run API tests, you can use:
```sh
./run_tests.py APITest
```

### Server Tests

The core functionality for server tests lives in the [tests/server](../tests/server) directory.
This includes a mock API server and a base test class that server tests can use to automatically start the mock server before tests.

#### API Tests

API tests directly make calls to the (mock) API server, and validates the output.
API tests live in [tests/api/testdata](../tests/api/testdata).
An API test is specified as a JSON file with the following fields:

| Key               | Requited | Default Value       | Type    | Description                             |
|-------------------|----------|---------------------|---------|-----------------------------------------|
| `module`          | true     | -                   | string  | The Python module (import path) for the API function. This file MUST define `API_ENDPOINT`, `API_PARAMS`, `send()` and `_get_parser()`. |
| `arguments`       | false    | {}                  | dict    | The arguments to send along with this API request. |
| `output-modifier` | false    | "clean_output_noop" | string  | A function to clean the output data before comparison. This is useful for things like normalizing times and randomly generated tokens. See [tests/api/test_api.py](../tests/api/test_api.py) for pre-defined functions. |
| `read-write`      | false    | false               | boolean | Set to true if this call should cause a write/update in the API server's data. This is used to speed up test data verification. |
| `error`           | false    | false               | boolean | Indicates that this call should return an error. |
| `output`          | true     | -                   | dict    | The response (content) if this API request. If `error` is true, then this should have the following keys: `code` (HTTP response code), `message` (the message sent by the API server), and `python-message` (the message inside the Python exception that was raised as a result of this call). |

To get the output of an API request,
the easiest way is to run your request on the command line (via one of the `autograder.cli.*` executables)
with the `--verbose` flag.
This will output the fill JSON request and response
(which you can then copy into the `output` field).

Since out test API data is the cornerstone of our server tests,
it is important to ensure that it is always correct.
To do this, we use the [.ci/verify_test_api_requests.py](../.ci/verify_test_api_requests.py) script.
Look at the script's `--help` output to see all of it's functionality.
The short version is that it creates a real Autograder API server to verify our test data.

During CI, this script will use a Docker image for the test server:
```
./.ci/verify_test_api_requests.py --docker
```

This method is not very fast, but should be consistent and portable to everywhere you can run docker.
The Docker image we used is built by the server on every tagged release.
The current version of the Docker image we used is specify in [.ci/backend.py](../.ci/backend.py) in the `DEFAULT_DOCKER_IMAGE` constant.
When you are targeting a new server version (like if you added an API endpoint), make sure to update the image version.

However, the Docker-based method is not as helpful for developers who also have changes pending on the server side
(since the Docker image will not be updated until changes are accepted).
This happens a lot when developers are adding a new API endpoint.
In this situation, you can run the verification script using an existing source directory for the server.
The script will build the server from this directory and use that to verify test data.

For example, if your Python interface repo (`autograder-py`) and server repo (`autograder-server`) are in the same directory,
then you can use a command like:
```
./.ci/verify_test_api_requests.py --source-dir ../autograder-server
```

#### CLI Tests

CLI tests are server tests that test the output (stdout) of the `autograder.cli.*` executables.
CLI tests live in [tests/cli/testdata](../tests/cli/testdata).
Like API tests, CLI tests use JSON-based options.
However, CLI tests are held in a hybrid JSON/txt file which also contains the expected output
(this allows users to easily include the output of the executable without worrying about special characters or newlines).
These files are split with a `---`,
where the upper part is the JSON options and the lower part is the expected output (stdout).

The JSON portion of the file has the following fields:

| Key            | Requited | Default Value    | Type    | Description                             |
|----------------|----------|------------------|---------|-----------------------------------------|
| `cli`          | true     | -                | string  | The Python module (import path) for the CLI main. This file MUST define `_get_parser()` and `run()`. |
| `arguments`    | false    | []               | dict    | String arguments to pass on the command line. |
| `output-check` | false    | "content_equals" | string  | The function that will be used to compare the actual output to the expected output. See [tests/cli/test_cli.py](../tests/cli/test_cli.py) for pre-defined functions. |
| `exit-status`  | false    | 0                | int     | The expected exit status. |
| `error`        | false    | false            | boolean | Indicates that this call should raise a Python exception. When set, then the expected output should match the message in the Python exception (instead of stdout). |
