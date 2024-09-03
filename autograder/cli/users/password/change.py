import getpass
import sys

import autograder.api.config
import autograder.api.users.password.change

def run(arguments):
    arguments = vars(arguments)

    if (arguments.get(autograder.api.config.PARAM_NEW_PASS.key, None) is None):
        arguments[autograder.api.config.PARAM_NEW_PASS.key] = _get_pass(arguments['stdin'])

    result = autograder.api.users.password.change.send(arguments, exit_on_error = True)

    if (result['duplicate']):
        print("Your new password must be different from your previous password.")
        return 1

    if (not result['success']):
        print("Your password was not changed.")
        return 2

    print("You have successfully changed your password.")
    return 0

def _get_pass(stdin):
    # Get the password from stdout without any prompt or confirmation.
    if (stdin):
        new_pass = ''
        while (len(new_pass) == 0):
            new_pass = sys.stdin.readline().strip()
        return new_pass

    # Use a prompt and confirmation.
    new_pass = ''
    confirmation = ''

    while ((len(new_pass) == 0) or (new_pass != confirmation)):
        new_pass = ''
        while (len(new_pass) == 0):
            new_pass = getpass.getpass('Password: ').strip()

        confirmation = ''
        while (len(confirmation) == 0):
            confirmation = getpass.getpass('Repeat Password: ').strip()

        if (new_pass != confirmation):
            print("Passwords do not match, try again.")

    return new_pass

def main():
    return run(_get_parser().parse_args())

def _get_parser():
    parser = autograder.api.users.password.change._get_parser()

    addendum = ('If no password is supplied on the command line,'
        + ' then you will be prompted for the password and confirmation.'
        + ' Use `-s`/`--stdin` to suppress the prompt (and confirmation),'
        + ' and just read the password from stdin.'
        + ' Space will be stripped off of password read through stdin'
        + ' (with or without `--stdin`.'
        + ' Empty passwords are not allowed.')

    parser.description += "\n\n" + addendum

    parser.add_argument('-s', '--stdin', dest = 'stdin',
        action = 'store_true', default = False,
        help = 'Suppress normal output and read the password from stdin (default: %(default)s)')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
