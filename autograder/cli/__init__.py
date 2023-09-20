import importlib

# Keep the dash (which is nice on the command-line), but give access to the module.
gradeassignment = importlib.import_module('autograder.cli.grade-assignment')
