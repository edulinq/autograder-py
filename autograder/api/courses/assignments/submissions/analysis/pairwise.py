import autograder.api.common
import autograder.api.config

def _submission_add_func(parser, param):
    parser.add_argument('submissions', metavar = 'SUBMISSION',
        action = 'store', type = str, nargs = '+',
        help = param.description)

API_ENDPOINT = 'courses/assignments/submissions/analysis/pairwise'
API_PARAMS = [
    autograder.api.config.PARAM_USER_EMAIL,
    autograder.api.config.PARAM_USER_PASS,

    autograder.api.config.APIParam('submissions',
        ('A list of submission specifications to analyze.'
        + ' Submissions may span courses and assignments.'
        + ' Submissions may be specified in three ways:'
        + ' 1) "<course id>::<assignment id>::<user email>::<submission short id>"'
        + ' for a specific submission,'
        + ' 2) "<course id>::<assignment id>::<user email>"'
        + ' for the given user\'s most recent submission to the given assignment,'
        + ' and 3) "<course id>::<assignment id>"'
        + ' for the most recent submission for all students.'),
        config_key = 'submissions', required = True,
        parser_add_func = _submission_add_func),

    autograder.api.config.APIParam('wait-for-completion',
            'Wait for the full analysis to complete before returning.',
            required = False,
            parser_options = {'action': 'store_true', 'default': False}),
]

DESCRIPTION = 'Get the result of a pairwise analysis for the specified submissions'

def send(arguments, **kwargs):
    return autograder.api.common.handle_api_request(arguments, API_PARAMS, API_ENDPOINT, **kwargs)

def _get_parser():
    parser = autograder.api.config.get_argument_parser(
        description = DESCRIPTION,
        params = API_PARAMS)

    return parser
