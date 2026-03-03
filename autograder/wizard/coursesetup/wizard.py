import os
import typing

import edq.util.dirent

import autograder.api.config
import autograder.api.metadata.heartbeat
import autograder.api.users.get
import autograder.error
import autograder.filespec
import autograder.wizard.commands
import autograder.wizard.model
import autograder.wizard.steps

class SetupData:
    """ A container for all the data used in this wizard. """

    def __init__(self, config: typing.Dict[str, typing.Any]) -> None:
        self.server: typing.Union[str, None] = config.get(autograder.api.config.PARAM_SERVER.config_key, None)
        """ The server to connect to. """

        self.user: typing.Union[str, None] = config.get(autograder.api.config.PARAM_USER_EMAIL.config_key, None)
        """ The user to connect as. """

        self.password: typing.Union[str, None] = config.get(autograder.api.config.PARAM_USER_PASS.config_key, None)
        """ The password to connect with. """

        self.source: typing.Union[autograder.filespec.FileSpec, None] = None
        """ The source for this course. """

        self.temp_dir: typing.Union[str, None] = None
        """ The path to a temp dir that will house the course. """

class ConnectStep(autograder.wizard.steps.SimpleInputStep):
    """ A step for connecting to an autograder server. """

    def __init__(self, data: SetupData) -> None:
        self._step_input_server: autograder.wizard.steps.SimpleInput = autograder.wizard.steps.SimpleInput(
            'address',
            'Enter the server to connect to',
            data.server,
        )
        """ Input for the server address. """

        self.data: SetupData = data
        """ The common data for this wizard. """

        super().__init__('Connect to Server', [
            self._step_input_server,
        ])

    def intro(self, wizard: autograder.wizard.model.BaseWizard) -> None:
        wizard.write("This step will connect to an existing Lynx Autograder server.")
        wizard.write("The server should be on and accessible from this machine.")
        wizard.write('')

    def post_input_action(self, wizard: autograder.wizard.model.BaseWizard) -> bool:
        server = self._step_input_server.value

        try:
            autograder.api.metadata.heartbeat.send({
                autograder.api.config.PARAM_SERVER.config_key: server,
            })
        except autograder.error.ConnectionError:
            wizard.error(f"Could not connect to autograder server at '{server}', check address and that the server is up.")
            return False

        self.data.server = server

        wizard.write(f"Successfully connected to autograder server at '{server}'.")

        return True

class AuthStep(autograder.wizard.steps.SimpleInputStep):
    """ A step for authenticating against an autograder server. """

    def __init__(self, data: SetupData) -> None:
        self._step_input_user: autograder.wizard.steps.SimpleInput = autograder.wizard.steps.SimpleInput(
            'user email',
            'Login Email',
            data.user,
            validation_func = autograder.wizard.steps.email_simple_input_validator,
        )
        """ Input for the user email. """

        self._step_input_password: autograder.wizard.steps.SimpleInput = autograder.wizard.steps.SimpleInput(
            'user password',
            'Login Password/Token',
            data.password,
        )
        """ Input for the user password. """

        self.data: SetupData = data
        """ The common data for this wizard. """

        super().__init__('Authenticate with Server', [
            self._step_input_user,
            self._step_input_password,
        ])

    def intro(self, wizard: autograder.wizard.model.BaseWizard) -> None:
        wizard.write("This step will authenticate your credentials against the autograder server.")
        wizard.write('')

    def post_input_action(self, wizard: autograder.wizard.model.BaseWizard) -> bool:
        server = self.data.server
        user_email = self._step_input_user.value
        password = self._step_input_password.value

        user = None
        try:
            user = autograder.api.users.get.send({
                autograder.api.config.PARAM_SERVER.config_key: server,
                autograder.api.config.PARAM_USER_EMAIL.config_key: user_email,
                autograder.api.config.PARAM_USER_PASS.config_key: password,
            })
        except autograder.error.AuthenticationError:
            wizard.error(f"Failed to authenticate as '{user_email}', please check your user and password.")
            return False

        if (user is None):
            wizard.error(f"Could not find user '{user_email}' on the server.")
            return False

        role = user.extra_fields.get('role', autograder.model.user.ServerRole.UNKNOWN)

        if (role < autograder.model.user.ServerRole.CREATOR):
            wizard.error(("You do not have the required permissions to create a course."
                    + f" You are a '{role}', and you need to be at least a '{autograder.model.user.ServerRole.CREATOR}'."))
            return False

        self.data.user = user_email
        self.data.password = password

        wizard.write(f"Successfully authenticated as '{user_email}'.")

        return True

class FetchSourceStep(autograder.wizard.steps.SimpleInputStep):
    """ A step for fetching this course from source. """

    # TODO - FileSpec link will change.
    def intro(self, wizard: autograder.wizard.model.BaseWizard) -> None:
        wizard.write("This step will attempt to fetch the course from its canonical home (we call a 'source').")
        wizard.write('Once a course is active on the autograder, it can be automatically updated using this source.')
        wizard.write('This wizard will fetch a copy of the course and put it in a temp directory.')
        wizard.write('Course sources are specified using File Specifications (FileSpecs):')
        wizard.write('    https://github.com/edulinq/autograder-server/blob/main/docs/types.md#file-specification-filespec')
        wizard.write('')

    def __init__(self, data: SetupData) -> None:
        default_source = None
        if (data.source is not None):
            default_source = str(data.source)

        self._step_input_source: autograder.wizard.steps.SimpleInput = autograder.wizard.steps.SimpleInput(
            'source',
            'Enter the source for this course',
            default_source,
        )
        """ Input for the source. """

        self.data: SetupData = data
        """ The common data for this wizard. """

        super().__init__('Fetch Course Source', [
            self._step_input_source,
        ])

    def post_input_action(self, wizard: autograder.wizard.model.BaseWizard) -> bool:
        source = self._step_input_source.value

        try:
            spec = autograder.filespec.parse(source)
        except autograder.filespec.FileSpecError as ex:
            wizard.error(f"Could not parse course source ('{source}'): '{ex}'.")
            return False

        temp_dir = edq.util.dirent.get_temp_dir('edq-ag-coursesetup-')
        out_dir = os.path.join(temp_dir, 'course')
        edq.util.dirent.mkdir(out_dir)

        try:
            autograder.filespec.copy(spec, temp_dir, out_dir, False)
        except Exception as ex:
            wizard.error(f"Failed to fetch course source ('{source}'): '{ex}'.")
            return False

        self.data.source = spec
        self.data.temp_dir = temp_dir

        wizard.write(f"Successfully copied course to temp dir: '{temp_dir}'.")

        return True

class CourseSetupWizard(autograder.wizard.model.BaseWizard):
    """
    A wizard for setting up an autograder course.
    """

    def __init__(self, config: typing.Dict[str, typing.Any]):
        self.data: SetupData = SetupData(config)
        """ The common data for this wizard. """

        steps: typing.List[autograder.wizard.model.BaseStep] = [
            ConnectStep(self.data),
            AuthStep(self.data),
            FetchSourceStep(self.data),
            # Build
            # Save / Commit

            # TEST
            autograder.wizard.steps.EchoStep(),
        ]

        super().__init__(
            steps = steps,
            commands = autograder.wizard.commands.COMMON_COMMANDS,
        )

    def intro(self) -> None:
        self.write("Welcome to the course setup wizard.")
        self.write("No data will be saved/committed until the final step.")
        self.write("Use :? or :help to see all available commands.")
        self.write("The exit, use `:quit` or Ctrl-C twice.")
