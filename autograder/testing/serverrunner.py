import logging
import typing

import edq.net.exchange
import edq.net.request
import edq.testing.serverrunner
import edq.util.parse
import edq.util.reflection

import autograder.api.common
import autograder.api.constants
import autograder.api.metadata.heartbeat
import autograder.cli.parser
import autograder.error
import autograder.model.config
import autograder.util.net

class ServerRunner(edq.testing.serverrunner.ServerRunner):
    """ A server runner specifically for the autograder server. """

    def __init__(self,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self._old_exchanges_clean_func: typing.Union[str, None] = None
        """
        The value of edq.net.exchange._exchanges_clean_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_set_exchanges_clean_func: bool = False
        """
        The value of autograder.cli.parser._set_exchanges_clean_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_make_request_exchange_complete_func: typing.Union[edq.net.exchange.HTTPExchangeComplete, None] = None
        """
        The value of edq.net.request._make_request_exchange_complete_func when start() is called.
        The original value may be changed in start(), and will be reset in stop().
        """

        self._old_serverrunner_logging_level: typing.Union[int, None] = None
        """
        The logging level for the edq server runner befoe tests are run.
        The original value may be changed in start(), and will be reset in stop().
        """

    def start(self) -> None:
        # Put the API in testing mode.
        autograder.api.common.set_testing_source_info()

        super().start()

        # Set configs.

        self._old_exchanges_clean_func = edq.net.exchange._exchanges_clean_func
        edq.net.exchange._exchanges_clean_func = edq.util.reflection.get_qualified_name(autograder.util.net.clean_api_response)

        self._old_set_exchanges_clean_func = autograder.cli.parser._set_exchanges_clean_func
        autograder.cli.parser._set_exchanges_clean_func = False

        def _make_request_callback(exchange: edq.net.exchange.HTTPExchange) -> None:
            # Restart if the request is a write.
            if (edq.util.parse.boolean(exchange.headers.get(autograder.api.constants.HEADER_KEY_WRITE, False))):
                self.restart()

        self._old_make_request_exchange_complete_func = edq.net.request._make_request_exchange_complete_func
        edq.net.request._make_request_exchange_complete_func = typing.cast(edq.net.exchange.HTTPExchangeComplete, _make_request_callback)

        # Disable logging from the runner, since it may disrupt CLI tests.
        logger = logging.getLogger('edq.testing.serverrunner')
        self._old_serverrunner_logging_level = logger.level
        logger.setLevel(logging.WARNING)

    def stop(self) -> bool:
        if (self._old_serverrunner_logging_level is not None):
            logger = logging.getLogger('edq.testing.serverrunner')
            logger.setLevel(self._old_serverrunner_logging_level)
            self._old_serverrunner_logging_level = None

        if (not super().stop()):
            return False

        # Restore old configs.

        edq.net.exchange._exchanges_clean_func = self._old_exchanges_clean_func
        self._old_exchanges_clean_func = None

        autograder.cli.parser._set_exchanges_clean_func = self._old_set_exchanges_clean_func
        self._old_set_exchanges_clean_func = False

        edq.net.request._make_request_exchange_complete_func = self._old_make_request_exchange_complete_func
        self._old_make_request_exchange_complete_func = None

        return True

    def identify_server(self) -> bool:
        # Check the server for a heartbeat.
        try:
            autograder.api.metadata.heartbeat.send(autograder.model.config.Config(server = self.server), exit_on_error = False)
        except autograder.error.ConnectionError:
            return False

        return True
