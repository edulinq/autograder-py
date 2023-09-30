import autograder.api.common

API_ENDPOINT = '/api/v01/user/list'
API_KEYS = ['user', 'pass', 'course']

def send(server, config_data):
    """
    Take in a server address
    and config data (of the form produced by autograder.api.common.parse_config()),
    and make a user list request.
    Returns:
        (success, <message or graded assignment>)
    """

    url = "%s%s" % (server, API_ENDPOINT)

    data = {}
    for key in API_KEYS:
        if (config_data.get(key) is None):
            return (False, "No request made, missing required config '%s'." % (key))

        data[key] = config_data[key]

    body, message = autograder.api.common.send_api_request(url, data = data)

    if (body is None):
        response = "The autograder failed to list users."
        response += "\nMessage from the autograder: " + message
        return (False, response)

    if (body['result'] is None):
        return (True, [])

    result = body['result']

    return (True, result)
