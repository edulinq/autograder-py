import autograder.api.common
import autograder.util.hash

API_ENDPOINT = '/api/v01/user/add'
API_KEYS = [
    'user', 'pass', 'course',
    'email', 'new-pass',
    'name', 'role',
    'force', 'send-email',
]

def send(server, config_data):
    """
    Take in a server address
    and config data (of the form produced by autograder.api.common.parse_config()),
    and make a user add request.
    Returns:
        (success, <message or graded assignment>)
    """

    url = "%s%s" % (server, API_ENDPOINT)

    data = {}
    for key in API_KEYS:
        if (config_data.get(key) is None):
            return (False, "No request made, missing required config '%s'." % (key))

        data[key] = config_data[key]

    if (data.get('new-pass', '') != ''):
        data['new-pass'] = autograder.util.hash.sha256_hex(data['new-pass'])

    body, message = autograder.api.common.send_api_request(url, data = data)

    if (body is None):
        response = "The autograder failed to try to add the user."
        response += "\nMessage from the autograder: " + message
        return (False, response)

    result = body

    return (True, result)
