"""
List the users on the server.
"""

import typing

import lms.model.users

import autograder.api.common
import autograder.api.config

API_ENDPOINT: str = 'users/list'
API_PARAMS: typing.List[autograder.api.config.APIParam] = [
    autograder.api.config.PARAM_SERVER,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.PARAM_SERVER_USER_REFERENCES.optional(),
]

def send(config: typing.Dict[str, typing.Any], **kwargs: typing.Any) -> typing.List[lms.model.users.ServerUser]:
    """ Send a request to the autograder. """

    response = autograder.api.common.make_api_request(API_ENDPOINT, config, API_PARAMS, **kwargs)

    # TEST
    import json
    print('---')
    print(json.dumps(response, indent = 4))
    print('---')

    users = []
    for raw_user in response['users']:
        raw_user['id'] = raw_user['email']
        users.append(lms.model.users.ServerUser(**raw_user))

    return sorted(users)
