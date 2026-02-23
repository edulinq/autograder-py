import json
import os

API_VERSION: str = 'v03'

API_REQUEST_JSON_KEY: str = 'content'

API_RESPONSE_KEY_SUCCESS: str = 'success'
API_RESPONSE_KEY_MESSAGE: str = 'message'
API_RESPONSE_KEY_STATUS: str = 'status'
API_RESPONSE_KEY_CONTENT: str = API_REQUEST_JSON_KEY
API_RESPONSE_KEY_SERVER_VERSION: str = 'server-version'

_THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
_VERSION_FILE: str = os.path.join(_THIS_DIR, '..', '..', 'testdata',
    'autograder-testdata', 'autograder-server', 'resources', 'VERSION.json')

with open(_VERSION_FILE, 'r') as _f:
    SUPPORTED_SERVER_VERSION: str = json.load(_f)['base-version']

HEADER_KEY_WRITE: str = 'edq-ag-write'
