import sys

import autograder.api.constants
import autograder.api.user.add
import autograder.cli.common
import autograder.util.hash

def run(arguments):
    arguments = vars(arguments)
    arguments['new-users'] = _load_users(arguments['path'])

    result = autograder.api.user.add.send(arguments, exit_on_error = True)

    autograder.cli.common.list_add_users(result, table = arguments['table'])
    return 0

def _load_users(path):
    users = []

    with open(path, 'r') as file:
        lineno = 0
        for line in file:
            lineno += 1

            line = line.strip()
            if (line == ""):
                continue

            parts = line.split("\t")
            if (len(parts) > 5):
                raise ValueError(
                    "File ('%s') line (%d) has too many values. Max is 5, found %d." % (
                        path, lineno, len(parts)))

            email = parts[0]

            password = ''
            if (len(parts) >= 2):
                password = parts[1]
                if (password != ''):
                    password = autograder.util.hash.sha256_hex(password)

            name = ''
            if (len(parts) >= 3):
                name = parts[2]

            role = 'unknown'
            if (len(parts) >= 4):
                role = parts[3]

            if (role not in autograder.api.constants.ROLES):
                raise ValueError(
                    "File ('%s') line (%d) has an invalid role '%s'." % (
                        path, lineno, role))

            lms_id = ''
            if (len(parts) >= 5):
                lms_id = parts[4]

            users.append({
                'email': email,
                'pass': password,
                'name': name,
                'role': role,
                'lms-id': lms_id,
            })

    return users

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.user.add._get_parser()

    parser.description = ('Add users to the course.'
            + ' When force is true, this becomes an upsert (update if exists, otherwise insert).')

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file where each line contains up to five columns:'
                + ' [email, pass, name, role, lms-id].'
                + ' Only the email is required.')

    parser.add_argument('--table', dest = 'table',
        action = 'store_true', default = False,
        help = 'Output the results as a TSV table with a header (default: %(default)s).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
