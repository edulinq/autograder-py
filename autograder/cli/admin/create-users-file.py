import argparse
import json
import os
import sys

import autograder.util.hash
import autograder.util.password

ROLES = [
    'other',
    'student',
    'grader',
    'admin',
    'owner',
]

def create_user(email, name = '', role = 'student', password = ''):
    email = email.strip()
    name = name.strip()

    role = role.strip().lower()
    if (role not in ROLES):
        raise ValueError("Unknown role: '%s'." % (role))

    if ((password is None) or (password == '')):
        password = autograder.util.password.rand_pass()
        print("Using passowrd: '%s'." % (password))

    hashpass = autograder.util.hash.sha256_hex(password)
    cryptpass, salt = autograder.util.password.hash(hashpass)

    return {
        'email': email,
        'name': name,
        'role': role,
        'pass': cryptpass,
        'salt': salt,
    }

def run(args):
    path = args.path
    users = {}

    if (os.path.isdir(path)):
        raise ValueError("Path already exists and is a dir: '%s'." % (path))

    if (os.path.isfile(path)):
        with open(path, 'r') as file:
            users = json.load(file)

    user = create_user(args.email, name = args.name, role = args.role, password = args.password)
    users[user['email']] = user

    with open(path, 'w') as file:
        json.dump(users, file, indent = 4)

def _get_parser():
    parser = argparse.ArgumentParser(description =
        "Create a users file, which can be used to seed users in a course."
        + " A full user must be specified, which will be added to the file."
        + " If an existing users file is specified, then the user will be added to the file.")

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to the new users JSON file.')

    parser.add_argument('email', metavar = 'EMAIL',
        action = 'store', type = str,
        help = 'Email for the new user.')

    parser.add_argument('-n', '--name', dest = 'name',
        action = 'store', type = str, default = '',
        help = 'Name for the new user.')

    parser.add_argument('-r', '--role', dest = 'role',
        action = 'store', type = str, default = 'student',
        help = 'Role for the new user. Defaults to student.')

    parser.add_argument('-p', '--pass', dest = 'password',
        action = 'store', type = str, default = '',
        help = 'Password for the new user. Defaults to a random string (will be output).')

    return parser

def main():
    return run(_get_parser().parse_args())

if (__name__ == '__main__'):
    sys.exit(main())
