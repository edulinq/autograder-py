import errno
import glob
import http
import http.server
import importlib
import json
import os
import re
import socket
import threading
import time
import urllib.parse

import requests_toolbelt.multipart.decoder

import autograder.api.config
import autograder.api.constants
import autograder.util.timestamp

START_PORT = 30000
END_PORT = 40000
ENCODING = 'utf8'

SLEEP_TIME_SEC = 0.2
REAP_TIME_SEC = 0.5

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = os.path.join(THIS_DIR, '..', '..')
API_BASE_DIR = os.path.join(ROOT_DIR, 'autograder', 'api')
API_TESTDATA_DIR = os.path.join(THIS_DIR, '..', 'api', 'testdata')

DATA_DIR_ID = '__DATA_DIR__'

INITIAL_BASE_ARGUMENTS = {
    'user': 'course-admin@test.edulinq.org',
    'pass': 'course-admin',
    'course': 'COURSE101',
    'assignment': 'hw0',

    # Will be set with the correct port when the test is run.
    'server': None,
}

_server = None

def start():
    port = _find_open_port()

    thread = threading.Thread(target = _run, args = (port,))
    thread.start()

    time.sleep(SLEEP_TIME_SEC)
    return thread, port

def stop(thread):
    global _server

    if (_server is not None):
        _server.shutdown()
        time.sleep(SLEEP_TIME_SEC)

    if (thread.is_alive()):
        thread.join(REAP_TIME_SEC)

def _find_open_port():
    for port in range(START_PORT, END_PORT + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('127.0.0.1', port))

            # Explicitly close the port and wait a short amount of time for the port to clear.
            # This should not be required because of the socket option above,
            # but the cost is small.
            sock.close()
            time.sleep(SLEEP_TIME_SEC)

            return port
        except socket.error as ex:
            sock.close()

            if (ex.errno == errno.EADDRINUSE):
                continue

            # Unknown error.
            raise ex

    raise ValueError("Could not find open port in [%d, %d]." % (START_PORT, END_PORT))

def _run(port):
    """
    Run the test server.
    """

    global _server

    _load_responses()

    _server = http.server.HTTPServer(('', port), Handler)
    _server.serve_forever(poll_interval = 0.1)

    _server.server_close()
    _server = None

def _load_responses():
    """
    Load API responses from the existing API test cases.
    """

    responses, api_modules_by_endpoint, api_modules_by_module = build_api_responses()

    Handler._api_modules_by_endpoint = api_modules_by_endpoint
    Handler._api_modules_by_module = api_modules_by_module
    Handler._static_responses = responses

def build_api_responses():
    """
    Look through the autograder/api/* packages for API endpoints
    and the API_TESTDATA_DIR directory for test data,
    and build up API responses and information about the API modeules.
    Response keys are just string JSON objects with the endpoint and args.

    Return:
       {<API reponse key>: { <response information> }, ...}
       {<API endpoint>: { <endpoint/module information> }, ...}
       {<API module name>: { <endpoint/module information> }, ...}
    """

    # First, build maps to lookup API endpoints.
    api_modules_by_endpoint, api_modules_by_module = _load_endpoint_modules()

    responses = {}

    for path in sorted(glob.glob(os.path.join(API_TESTDATA_DIR, "**", "*.json"), recursive = True)):
        with open(path, 'r') as file:
            data = json.load(file)

        for required_key in ['module', 'output']:
            if (required_key not in data):
                raise ValueError("Found API test data without key '%s': '%s'." % (
                    required_key, path))

        api_module_info = api_modules_by_module.get(data['module'])
        if (api_module_info is None):
            raise ValueError("Could not find module for module name '%s'." % (data['module']))

        key = _create_request_lookup_key(api_module_info,
            data.get('arguments', {}), data.get('files', []),
            normalize_args = True)

        if (key in responses):
            raise ValueError("Duplicate response key '%s' found in '%s'." % (key, path))

        responses[key] = {
            'endpoint': api_module_info['endpoint'],
            'module_name': data['module'],
            'arguments': data.get('arguments', {}),
            'output': data['output'],
        }

    return responses, api_modules_by_endpoint, api_modules_by_module

def _load_endpoint_modules():
    """
    Load all the modules in autograder/api/* looking for API endpoint modules,
    which all have API_ENDPOINT and API_PARAMS constants.
    Load these modules into maps for lookup by endpoint and module name (qualified import name).
    """

    api_modules_by_endpoint = {}
    api_modules_by_module = {}

    for path in sorted(glob.glob(os.path.join(API_BASE_DIR, '**', '*.py'), recursive = True)):
        filename = os.path.basename(path)
        if (filename.startswith('__')):
            continue

        relpath = os.path.relpath(path, API_BASE_DIR)

        import_module_name = re.sub(r'\.py$', '', relpath)
        import_module_name = import_module_name.replace('/', '.')
        import_module_name = 'autograder.api.' + import_module_name

        api_module = importlib.import_module(import_module_name)

        if (not hasattr(api_module, 'API_ENDPOINT')):
            # Not an API endpoint module.
            continue

        data = {
            'module': api_module,
            'endpoint': api_module.API_ENDPOINT,
            'module_name': import_module_name,
            'params': api_module.API_PARAMS,
        }

        api_modules_by_endpoint[api_module.API_ENDPOINT] = data
        api_modules_by_module[import_module_name] = data

    return api_modules_by_endpoint, api_modules_by_module

def _create_request_lookup_key(api_module_info, arguments, files, normalize_args = False):
    """
    Build a key that can be used to uniquely identify an API request.
    """

    if (normalize_args):
        # Build an accurate representation of the arguments this request would send.
        full_arguments = INITIAL_BASE_ARGUMENTS.copy()
        full_arguments.update(arguments)

        # Fill in a dummy server so it passed validation.
        # This is not part of the formal arguments and will get stripped.
        full_arguments['server'] = 'dummy'

        # Pass the arguments through the same infrastructure as the API.
        config = autograder.api.config.get_tiered_config(full_arguments)
        arguments, _ = autograder.api.config.parse_api_config(config, api_module_info['params'])

    key = {
        'endpoint': api_module_info['endpoint'],
        'arguments': arguments,
        'files': files,
    }

    key = json.dumps(key, sort_keys = True, separators = (',', ':'))

    return key

class Handler(http.server.BaseHTTPRequestHandler):
    # Maps that can lookup API modules by module name and endpoint.
    _api_modules_by_endpoint = {}
    _api_modules_by_module = {}

    # All known responses keyed by _create_request_lookup_key().
    _static_responses = {}

    def log_message(self, format, *args):
        return

    def do_POST(self):
        request_data, request_files = self._get_request_data()

        path = self.path
        endpoint = re.sub(r'^/api/v\d+/', '', path)

        headers = {}
        content = self._get_response(endpoint, request_data, request_files)
        message = content.get('message', "")
        code = content.get('code', http.HTTPStatus.OK)

        now = autograder.util.timestamp.get()

        data = {
            "id": "00000000-0000-0000-0000-000000000000",
            "locator": "",
            "server-version": "0.0.0",
            "start-timestamp": now,
            "end-timestamp": now,
            "status": code,
            autograder.api.constants.API_RESPONSE_KEY_SUCCESS: (code == http.HTTPStatus.OK),
            autograder.api.constants.API_RESPONSE_KEY_MESSAGE: message,
            autograder.api.constants.API_RESPONSE_KEY_CONTENT: content,
        }

        payload = json.dumps(data)

        self.send_response(code)

        for (key, value) in headers:
            self.send_header(key, value)
        self.end_headers()

        self.wfile.write(payload.encode(ENCODING))

    def _get_request_data(self):
        data = {}
        files = []

        content_type = self.headers.get('Content-Type', '')
        length = int(self.headers['Content-Length'])
        raw_content = self.rfile.read(length)

        if (content_type == 'application/x-www-form-urlencoded'):
            request = urllib.parse.parse_qs(raw_content.decode(ENCODING))
            data = json.loads(request[autograder.api.constants.API_REQUEST_JSON_KEY][0])
            return data, files

        if (content_type.startswith('multipart/form-data')):
            decoder = requests_toolbelt.multipart.decoder.MultipartDecoder(
                raw_content, content_type, encoding = ENCODING)

            for part in decoder.parts:
                values = _parse_disposition(part.headers)

                if (values.get('name', ()) == autograder.api.constants.API_REQUEST_JSON_KEY):
                    data = json.loads(part.text)
                else:
                    # Assume everything else is a file.
                    filename = values.get('filename', '')
                    if (filename == ''):
                        raise ValueError("Unable to find filename for request.")

                    files.append("%s(%s)" % (DATA_DIR_ID, filename))

            return data, files

        raise ValueError("Unknown content type: '%s'." % (content_type))

    def _get_response(self, endpoint, data, files):
        api_module_info = Handler._api_modules_by_endpoint.get(endpoint)
        if (api_module_info is None):
            raise ValueError("Could not find module for endpoint '%s'." % (endpoint))

        key = _create_request_lookup_key(api_module_info, data, files, normalize_args = False)
        if (key not in Handler._static_responses):
            raise ResponseKeyError(key)

        return Handler._static_responses[key]['output']

def _parse_disposition(headers):
    values = {}
    for (key, value) in headers.items():
        key = key.decode(ENCODING)
        value = value.decode(ENCODING)

        if (key.lower() != 'content-disposition'):
            continue

        # The python stdlib recommends using the email library for this parsing,
        # but I have not had a good experience with it.
        for part in value.strip().split(';'):
            part = part.strip()

            parts = part.split('=')
            if (len(parts) != 2):
                continue

            cd_key = parts[0].strip()
            cd_value = parts[1].strip().strip('"')

            values[cd_key] = cd_value

    return values

class ResponseKeyError(ValueError):
    def __init__(self, key):
        super().__init__("Could not find API response for key '%s'." % (key))
        self._key = key

    def __str__(self):
        lines = []

        key_str = json.dumps(json.loads(self._key), indent = 4)

        known_keys = list(sorted(Handler._static_responses.keys()))
        known_keys = [json.loads(known_key) for known_key in known_keys]

        known_keys = sorted(known_keys, key = lambda key: key['endpoint'])

        lines.append("Could not find API response for key:\n%s\n" % (key_str))
        lines.append("All known keys are below (sorted by endpoint).")
        lines.append("All fields must match for the server to find the proper response.")
        lines.append("Ensure that the proper API test case exists for your desired response.")
        lines.append("--- BEGIN Known Keys ---")
        lines.append(json.dumps(known_keys, indent = 4))
        lines.append("--- END Known Keys ---")

        return "\n".join(lines)
