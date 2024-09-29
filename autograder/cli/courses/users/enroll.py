import sys

import autograder.api.config
import autograder.api.courses.users.enroll
import autograder.cli.common
import autograder.cli.config

def run(arguments):
    arguments = vars(arguments)

    arguments['raw-course-users'] = [{
        'email': arguments['new-email'],
        'name': arguments['new-name'],
        'course-role': arguments['new-course-role'],
        'course-lms-id': arguments['new-lms-id'],
    }]

    arguments['send-emails'] = not arguments['skip-emails']

    result = autograder.api.courses.users.enroll.send(arguments, exit_on_error = True)

    autograder.cli.common.list_user_op_responses(result['results'], table = arguments['table'])
    return 0

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.courses.users.enroll._get_parser()

    autograder.cli.config.add_table_argument(parser)
    autograder.cli.config.add_skip_emails_argument(parser)

    autograder.cli.config.add_new_email_argument(parser, "enroll")
    autograder.cli.config.add_new_name_argument(parser, "enroll")
    autograder.cli.config.add_new_course_role_argument(parser, "enroll")
    autograder.cli.config.add_new_lms_id_argument(parser, "enroll")

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
