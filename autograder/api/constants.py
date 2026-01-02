import typing

API_VERSION: str = 'v03'

API_REQUEST_JSON_KEY: str = 'content'

API_RESPONSE_KEY_SUCCESS: str = 'success'
API_RESPONSE_KEY_MESSAGE: str = 'message'
API_RESPONSE_KEY_STATUS: str = 'status'
API_RESPONSE_KEY_CONTENT: str = API_REQUEST_JSON_KEY

HEADER_KEY_WRITE: str = 'edq-ag-write'

SERVER_ROLES: typing.List[str] = [
    'user',
    'creator',
    'admin',
    'owner',
]

COURSE_ROLES: typing.List[str] = [
    'unknown',
    'other',
    'student',
    'grader',
    'admin',
    'owner',
]
