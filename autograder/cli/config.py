import autograder.api.constants

# Common CLI arguments.

def add_new_course_role_argument(parser, action):
    parser.add_argument('--new-course-role', dest = 'new-course-role',
        action = 'store', type = str, default = 'student',
        choices = autograder.api.constants.COURSE_ROLES,
        help = f'The course role of the user to {action} (default: %(default)s).')

def add_new_email_argument(parser, action):
    parser.add_argument('--new-email', dest = 'new-email',
        action = 'store', type = str, required = True,
        help = f'The email of the user to {action}.')

def add_new_lms_id_argument(parser, action):
    parser.add_argument('--new-lms-id', dest = 'new-lms-id',
        action = 'store', type = str, default = '',
        help = f'The lms id of the user to {action}.')

def add_new_name_argument(parser, action):
    parser.add_argument('--new-name', dest = 'new-name',
        action = 'store', type = str, default = '',
        help = f'The name of the user to {action}.')

def add_skip_emails_argument(parser):
    parser.add_argument('--skip-emails', dest = 'skip-emails',
        action = 'store_true', default = False,
        help = 'Skip sending any emails. Be aware that this may result in inaccessible'
        + ' information (default: %(default)s).')

def add_table_argument(parser):
    parser.add_argument('--table', dest = 'table',
        action = 'store_true', default = False,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')
