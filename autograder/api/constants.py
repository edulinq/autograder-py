import os

import edq.util.json

API_VERSION: str = 'v03'

API_REQUEST_JSON_KEY: str = 'content'

API_RESPONSE_KEY_SUCCESS: str = 'success'
API_RESPONSE_KEY_MESSAGE: str = 'message'
API_RESPONSE_KEY_STATUS: str = 'status'
API_RESPONSE_KEY_CONTENT: str = API_REQUEST_JSON_KEY
API_RESPONSE_KEY_SERVER_VERSION: str = 'server-version'

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
VERSION_FILE: str = os.path.join(THIS_DIR, 'version.json')

SUPPORTED_SERVER_VERSION: str = edq.util.json.load_path(VERSION_FILE)['base-version']

HEADER_KEY_WRITE: str = 'edq-ag-write'
