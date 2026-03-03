import typing

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
            wizard.error(("You do not have the required premissions to create a course."
                    + f" You are a '{role}', and you need to be at least a '{autograder.model.user.ServerRole.CREATOR}'."))
            return False

        self.data.user = user_email
        self.data.password = password

        wizard.write(f"Successfully authenticated as '{user_email}'.")

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
            # FetchSourceStep(self.data),
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
