import autograder.api.common
import autograder.api.config 

API_ENDPOINT = 'courses/assignments/list'
API_PARAMS = [
    autograder.api.config.PARAM_COURSE_ID,
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS
]

DESCRIPTION = 'List the assignments in the course'

# Main function 
def send(arguments: dict, **kwargs) -> dict:
    return autograder.api.common.handle_api_request(
        arguments,      # User args (course, user pass)
        API_PARAMS,     # Our required/optional params 
        API_ENDPOINT,   # Endpoint name 
        **kwargs        # Additional args ex files 
    )


# CLI support 
def _get_parser(): 
    """
    Creates and returns an argument parser for the CLI 
    """

    parser = autograder.api.config.get_argument_parser(
        description=DESCRIPTION,
        params=API_PARAMS
    )

    return parser