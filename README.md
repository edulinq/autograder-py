# Python Interface for Autograder

The canonical Python interface for the autograding server.

## Quick Links

 - [Resources](#resources)
 - [Installation / Requirements](#installation--requirements)
 - [Quickstart](#quickstart)
 - [The CLI](#the-cli)
   - [Configuration](#configuration)
   - [Commands for Students](#commands-for-students)
     - [Submitting an Assignment](#submitting-an-assignment)
       - [Submitting an Assignment Late](#submitting-an-assignment-late)
     - [Checking Your Last Submission](#checking-your-last-submission)
     - [Getting a History of All Past Submissions](#getting-a-history-of-all-past-submissions)
     - [Managing your Password](#managing-your-password)
   - [Commands for TAs and Instructors](#commands-for-tas-and-instructors)
   - [Commands for Course Builders](#commands-for-course-builders)

## Resources

 - [Autograder Server](https://github.com/edulinq/autograder-server)
 - [Autograder Python Interface (this repo)](https://github.com/edulinq/autograder-py)
 - [Autograder Sample Course](https://github.com/edulinq/cse-cracks-course)

## Installation / Requirements

This project requires [Python](https://www.python.org/) >= 3.8.

The project can be installed from PyPi with:
```
pip3 install autograder-py
```

Standard Python requirements are listed in `pyproject.toml`.
The project and Python dependencies can be installed from source with:
```
pip3 install .
```

## Quickstart

To provide easy access to a limited number of commands,
we provide the `autograder.run` suite of shortcuts.
These are just a small number of the most commonly used commands.
For a more in-depth look at the available commands,
see the [cli section](#the-cli) of this document.

### `autograder.run.submit`

This command sends an assignment submission to the server.
This is a shortcut for [`autograder.cli.courses.assignments.submissions.submit`](#submitting-an-assignment).

```sh
python3 -m autograder.run.submit my_file.py
```

To submit an assignment late, use the following command.
For more information and examples, see the [late submission section](#submitting-an-assignment-late) of this document.

```sh
python3 -m autograder.run.submit --allow-late my_file.py
```

### `autograder.run.history`

This command gets a summary of all your past submissions for an assignment.
This is a shortcut for [`autograder.cli.courses.assignments.submissions.user.history`](#getting-a-history-of-all-past-submissions).

```sh
python3 -m autograder.run.history
```

### `autograder.run.peek`

This command shows you your most recent (or a specific) submission for an assignment.
This is a shortcut for [`autograder.cli.courses.assignments.submissions.user.peek`](#checking-your-last-submission).

```sh
python3 -m autograder.run.peek
```

To get a specific submission, just pass the submission ID (as shown in `autograder.run.history`).

```sh
python3 -m autograder.run.peek 123456789
```

### `autograder.run.auth`

You can use this command to quickly check if your password/config is correct.
This is a shortcut for `autograder.cli.users.auth`.

```sh
python3 -m autograder.run.auth
```

### `autograder.run.change-pass`

This command lets your change your password to whatever you want.
This is a shortcut for [`autograder.cli.users.pass.change`](#managing-your-password).

```sh
python3 -m autograder.run.change-pass
```

You will then be prompted to enter (and re-enter) your new password.

### `autograder.run.reset-pass`

This command will reset your password by sending an email to your registered email address.
This is a shortcut for [`autograder.cli.users.pass.reset`](#managing-your-password).

```sh
python3 -m autograder.run.reset-pass
```

## The CLI

This project contains several tools for interacting with an autograding server and
working with autograder assignments via the `autograder.cli` package.
All tools will show their usage if given the `--help` options.

You can get a list of the package for each set of tools by invoking `autograder.cli` directly:
```sh
python3 -m autograder.cli
```

If you want to see every tool a package (and all its subpackages) have available in one output,
you can use the `-r`/`--recursive` flag:
```sh
python3 -m autograder.cli --recursive
```

There are many available tools and instead of discussing each one here,
this document will highlight the tools each type of user (student, TA, course developer) will generally use.

### Configuration

Before discussing specific tools, you should know some general information about
configuring and sending options to each tool.

To know who you are and what you are working on the autograder needs a few configuration options:
 - `server` -- The autograding server to connect to.
 - `course` -- The ID for the course you are enrolled in.
 - `assignment` -- The current assignment you are working on (does not always apply)..
 - `user` -- Your username (which is also your email).
 - `pass` -- Your password (probably sent to you by the autograding server in an email).

All these options can be set on the command line when invoking on of these tools, e.g.,:
```sh
python3 -m autograder.run.submit --user sammy@ucsc.edu --pass pass123 my_file.py
```
However, it will generally be more convenient to hold these common options in a more reusable location.

There are several other places that config options can be specified,
with each later location overriding any earlier options.
Here are the places options can be specified in the order that they are checked:
 1. `./config.json` -- If a `config.json` exists in the current directory, it is loaded.
 2. `<platform-specific user config location>/autograder.json` -- A directory which is considered the "proper" place to store user-related config for the platform you are using (according to [platformdirs](https://github.com/platformdirs/platformdirs)). Use `--help` to see the exact place in your specific case. This is a great place to store login credentials.
 3. Files specified by `--config` -- These files are loaded in the order they appear on the command-line.
 4. Bare Options -- Options specified directly like `--user` or `--pass`. These will override all previous options.

A base config file (`config.json`) is often distributed with assignments that contains most the settings you need.
You can modify this config to include your settings and use that for setting all your configuration options.
A `config.json` file may look something like:
```json
{
    "course": "my-course",
    "assignment": "assignment-01",
    "server": "http://fake.autograder.edulinq.org",
    "user": "user@edulinq.org",
    "pass": "1234567890"
}
```

Using the default config file (`config.json`):
```sh
# `./config.json` will be looked for and loaded if it exists.
python3 -m autograder.run.submit my_file.py
```

Using a custom config file (`my_config.json`):
```sh
# `./my_config.json` will be used.
python3 -m autograder.run.submit --config my_config.json my_file.py
```

You can also use multiple config files (latter files will override settings from previous ones).
This is useful if you want to use the config files provided with assignments, but keep your user credentials in a more secure location:
```sh
# Use the default config file (config.json), but then override any settings in there with another config file:
python3 -m autograder.run.submit --config config.json --config ~/.secrets/autograder.json my_file.py
```

For brevity, all future commands in this document will assume that all standard config options are in the default
config files (and thus will not need to be specified).

### Commands for Students

Students will mainly be concerned with submitting assignments and checking on the status of their submission.
Therefore, the `autograder.run` package will be their primary resource.
This package contains tools for making, managing, and querying submissions.

#### Submitting an Assignment

Submitting an assignment to an autograder is done using the `autograder.run.submit` command.
This command takes the standard config options as well as an optional message to attach to the submission (like a commit message)
as well as all files to be included in the submission.

```sh
python3 -m autograder.run.submit --message "This is my submit message!" my_file.py
```

As many files as you need can be submitted (directories cannot be submitted):
```sh
python3 -m autograder.run.submit my_first_file.py my_second_file.java some_dir/*
```

The autograder will attempt to grade your assignment and will return some message about the result of grading.
For example, a successful grading may look like:
```
The autograder successfully graded your assignment.
Autograder transcript for assignment: HO0.
Grading started at 2023-09-26 08:35 and ended at 2023-09-26 08:35.
Task 1.A (my_function): 40 / 40
Task 2.A (test_my_function_value): 30 / 30
Task 2.B (TestMyFunction): 30 / 30
Style: 0 / 0
   Style is clean!

Total: 100 / 100
```

On any successful grading (even if you got a zero), your result has been saved by the autograder and is in the system.
On a submission failure, the autograder will tell you and you will not receive any grade for your submission.
A failure may look like:
```
The autograder failed to grade your assignment.
Message from the autograder: Request could not be authenticated. Ensure that your username, password, and course are properly set.
```

##### Submitting an Assignment Late

If you are submitting an assignment late, the autograder requires confirmation in order to grade your submission.
This helps users avoid situations where they accidentally submit an assignment late or submit to the wrong assignment.
Users must add the `--allow-late` flag to the normal submission command when they want to submit an assignment past the due date.

For example, your output when submitting a late assignment may look like:
```
--- Message from Autograder ---
Attempting to submit assignment (HO0) late without the 'allow late' option.
It was due on 2024-12-13 16:00 (which was 48h34m57.178s ago).
Use the 'allow late' option to submit an assignment late.
See your interface's documentation for more information.
-------------------------------
Submission was rejected by the autograder.
```

When you see this message, be sure to double check the assignment name and due date.
If those details look correct and you want to submit that assignment late, then run the following command:
```sh
python3 -m autograder.run.submit --allow-late my_file.py
```

Now, the server will grade your late submission like normal!

#### Checking Your Last Submission

You can ask the autograder to show you the grade report for your last submission using the
`autograder.run.peek` command.

```sh
python3 -m autograder.run.peek
```

The output may look like:
```
Found a past submission for this assignment.
Autograder transcript for assignment: HO0.
Grading started at 2023-09-26 08:35 and ended at 2023-09-26 08:35.
Task 1.A (my_function): 40 / 40
Task 2.A (test_my_function_value): 30 / 30
Task 2.B (TestMyFunction): 30 / 30
Style: 0 / 0
   Style is clean!

Total: 100 / 100
```

If you have made no past (successful) submissions, then your output may look like:
```
No matching submission found.
```

#### Getting a History of All Past Submissions

You can use the `autograder.run.history` command to get a summary of all your past submissions for an assignment.

```sh
python3 -m autograder.run.history
```

The output may look like:
```
Found 2 submissions.
    Submission ID: 1695682455, Score: 24 / 100, Time: 2023-09-25 17:54.
    Submission ID: 1695735313, Score: 100 / 100, Time: 2023-09-26 08:35, Message: 'I did it!'
```

If you have made no past (successful) submissions, then your output may look like:
```
No matching submission found.
```

#### Managing your Password

Your password is the same throughout a single instance of the autograding server.
This means that multiple courses that run on the same server will all use your same account
(and therefore password).

Your initial password should have been emailed to the email associated with your account
(typically your school email address).

To reset your password,
use the `autograder.run.reset-pass` (aka `autograder.cli.users.pass.reset`) command:

```sh
python3 -m autograder.run.reset-pass
```

This will email you a new random password to your account's email.
Once your password is reset, it is recommended to change it to whatever you want.

To change your password, you can use the
`autograder.run.change-pass` (aka `autograder.cli.users.pass.change`) command:

```sh
python3 -m autograder.run.change-pass
```

You will then be prompted to enter (and re-enter) your new password.
See the command's help prompt (`--help`) for additional ways you can supply your password.

### Commands for TAs and Instructors

For those that are managing a course and students,
most commands will be useful to you.
So you should have a look through all commands via:
```sh
python3 -m autograder.cli -r
```

This will list all available packages and commands.
You can omit the `-r` if you want to look at one package at a time.
For example, to inspect the `autograder.run` package, you can do:
```sh
python -m autograder.run
```

Below is a list of commands you may want to look into.
The help prompt of each command (accessible using the `--help` option)
will give a more in-depth description of the command and available options.

 - `autograder.lms.upload-scores` -- Upload scores for any LMS assignment straight to your LMS. Very useful for avoiding a clunky LMS interface.
 - `autograder.cli.courses.assignments.submissions.fetch.course.scores` -- Get all the most recent scores for an assignment.
 - `autograder.cli.courses.assignments.submissions.fetch.user.attempt` -- Get a student's submission (code) and grading output.
 - `autograder.cli.courses.assignments.submissions.fetch.course.attempts` -- Get all the most recent submissions (code and grading output) for an assignment.
 - `autograder.cli.courses.users.list` -- List all the users in a course.

### Commands for Course Builders

Users who are building courses should generally be aware of all the available tools,
but most of your time will probably be spent in the
`autograder.cli.testing` and `autograder.cli.grading` packages.
`autograder.cli.testing` is for running tests and checks (usually locally) on assignments.
`autograder.cli.grading` lets you grade assignments locally (without using an autograding server).
Because the autograding server runs this package inside a Docker container to do grading,
it can be much faster and more convenient to build assignments fully locally before using an autograding server.
