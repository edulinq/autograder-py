import sys

def main():
    print(("You have invoked the `autograder` package directly."
        + " You probably want the `autograder.cli` package instead."))
    return 0

if (__name__ == '__main__'):
    sys.exit(main())
