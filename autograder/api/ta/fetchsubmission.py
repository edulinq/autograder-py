import autograder.api.common
import autograder.assignment

API_ENDPOINT = '/api/v01/submission/fetch'
API_KEYS = ['user', 'pass', 'course', 'assignment', 'email']

def send(server, config_data):
    """
    Take in a server address
    and config data (of the form produced by autograder.api.common.parse_config()),
    and make a fetch submission request.
    Returns:
        (success, <message or map of email -> submission summary>)
    """

    url = "%s%s" % (server, API_ENDPOINT)

    data = {}
    for key in API_KEYS:
        if (config_data.get(key) is None):
            return (False, "No request made, missing required config '%s'." % (key))

        data[key] = config_data[key]

    body, message = autograder.api.common.send_api_request(url, data = data)

    if (body is None):
        response = "The autograder failed to get a submission."
        response += "\nMessage from the autograder: " + message
        return (False, response)

    result = body

    return (True, result)
