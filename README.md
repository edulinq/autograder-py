# Python Interface for Autograder

The Python interface for the autograding server.

## The CLI

This project contains several tools for interacting with an autograding server and
working with autograder assignments via the `autograder.cli` package.
All tools will show their usage if given the `--help` options.

You can get a list of the package for each set of tools by invoking `autograder.cli` directly:
```sh
python3 -m autograder.cli
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
 - `pass` -- You password (probably sent to you by a TA or the autograding server in an email).

All these options can be set on the command line when invoking on of these tools, e.g.,:
```sh
python3 -m autograder.cli.submission.submit --user sammy@ucsc.edu --pass pass123 my_file.py
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

Using the default config file (`config.json`):
```sh
# `./config.json` will be looked for and loaded if it exists.
python3 -m autograder.cli.submission.submit my_file.py
```

Using a custom config file (`my_config.json`):
```sh
# `./my_config.json` will be used.
python3 -m autograder.cli.submission.submit --config my_config.json my_file.py
```

You can also use multiple config files (latter files will override settings from previous ones).
This is useful if you want to use the config files provided with assignments, but keep your user credentials in a more secure location:
```sh
# Use the default config file (config.json), but then override any settings in there with another config file:
python3 -m autograder.cli.submission.submit --config config.json --config ~/.secrets/autograder.json my_file.py
```

For brevity, all future commands in this document will assume that all standard config options are in the default
config files (and thus will not need to be specified).

### Commands for Students

Students will mainly be concerned with submitting assignments and checking on the status of their submission.
Therefore, the `autograder.cli.submission` package will be their primary resource.
This package contains tools for making, managing, and querying submissions.

#### Submitting an Assignment

Submitting an assignment to an autograder is done using the `autograder.cli.submission.submit` command.
This command takes the standard config options as well as an optional message to attach to the submission (like a commit message)
as well as all files to be included in the submission.

```sh
python3 -m autograder.cli.submission.submit --message "This is my submit message!" my_file.py
```

As many files as you need can be submitted (directories cannot be submitted):
```sh
python3 -m autograder.cli.submission.submit my_first_file.py my_second_file.java some_dir/*
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

#### Checking Your Last Submission

You can ask the autograder to show you the grade report for your last submission using the
`autograder.cli.submission.peek` command.

```sh
python3 -m autograder.cli.submission.peek
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
No past submission found for this assignment.
```

#### Getting a History of All Past Submissions

You can use the `autograder.cli.submission.history` command to get a summary of all your past submissions for an assignment.

```sh
python3 -m autograder.cli.submission.history
```

The output may look like:
```
Found 2 submissions.
    Submission ID: 1695682455, Score: 24 / 100, Time: 2023-09-25 17:54.
    Submission ID: 1695735313, Score: 100 / 100, Time: 2023-09-26 08:35, Message: 'I did it!'
```

If you have made no past (successful) submissions, then your output may look like:
```
No past submission found for this assignment.
```

### Commands for TAs and Instructors

For those that are managing a course and students,
most commands will be useful to you.
So you should have a look through all commands via:
```sh
python3 -m autograder.cli
```

Below is a list of commands you may want to look into.
The help prompt of each command (accessible using the `--help` option)
will give a more in-depth description of the command and available options.

 - `autograder.lms.sync-users` -- Get information about users from your LMS (e.g. Canvas).
 - `autograder.lms.upload-scores` -- Upload scores for any LMS assignment straight to your LMS. Very useful for avoiding a clunky LMS interface.
 - `autograder.submission.fetch-scores` -- Get all the most recent scores for an assignment.
 - `autograder.submission.fetch-submission` -- Get a student's submission (code) and grading output.
 - `autograder.submission.fetch-submissions` -- Get all the most recent submissions (code and grading output) for an assignment.
 - `autograder.user.*` -- Several different tools for managing users (adding, removing, changing passwords, etc).

### Commands for Course Builders

Users who are building courses should generally be aware of all the available tools,
but most of your time will probably be spent in the
`autograder.cli.testing` and `autograder.cli.grading` packages.
`autograder.cli.testing` is for running tests and checks (usually locally) on assignments.
`autograder.cli.grading` lets you grade assignments locally (without using an autograding server).
Because the autograding server runs this package inside a Docker container to do grading,
it can be much faster and more convenient to build assignments fully locally before using an autograding server.
