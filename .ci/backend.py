import abc
import atexit
import os
import signal
import subprocess
import sys
import time

THIS_DIR = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR = os.path.join(THIS_DIR, '..')

# Add in the root path.
sys.path.append(ROOT_DIR)

import util

DEFAULT_PORT = 8080
WEB_URL = 'http://127.0.0.1'

DEFAULT_DOCKER_IMAGE = 'ghcr.io/edulinq/autograder-server:3.4.7-prebuilt'
DOCKER_CONTAINER_NAME = 'autograder-py-verify-test-data'
DOCKER_START_SLEEP_TIME_SECS = 0.25
DOCKER_STOP_WAIT_TIME_SECS = 1
DOCKER_STOP_FINAL_WAIT_TIME_SECS = 0.5

SOURCE_START_SLEEP_TIME_SECS = 0.25
SOURCE_KILL_SLEEP_TIME_SECS = 0.25

class BaseServer(abc.ABC):
    def __init__(self, port = DEFAULT_PORT, **kwargs):
        self._port = port

    @abc.abstractmethod
    def start(self, **kwargs):
        pass

    @abc.abstractmethod
    def stop(self, **kwargs):
        pass

    @abc.abstractmethod
    def reset(self, **kwargs):
        pass

    def get_address(self):
        return "%s:%d" % (WEB_URL, self._port)

class WebServer(BaseServer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start(self, **kwargs):
        pass

    def stop(self, **kwargs):
        pass

    def reset(self, araguments = {}, **kwargs):
        pass

class DockerServer(BaseServer):
    def __init__(self, image = DEFAULT_DOCKER_IMAGE, **kwargs):
        super().__init__(**kwargs)

        self._image = image
        self._is_running = False

        # Before starting the server the first time,
        # ensure the image is up-to-date (only if we are using the default image).
        if (self._image == DEFAULT_DOCKER_IMAGE):
            self._pull_image()

        # Try to stop the server on termination.
        atexit.register(self.stop)

    def start(self, **kwargs):
        args = self._get_base_args() + ['server', '--unit-testing']

        util.run(args)

        self._is_running = True
        time.sleep(DOCKER_START_SLEEP_TIME_SECS)

    def stop(self, **kwargs):
        if (not self._is_running):
            return

        args = [
            'docker', 'stop',
            '--time', str(int(DOCKER_STOP_WAIT_TIME_SECS)),
            DOCKER_CONTAINER_NAME,
        ]

        util.run(args)
        time.sleep(DOCKER_STOP_FINAL_WAIT_TIME_SECS)
        self._is_running = False

    def reset(self, **kwargs):
        # Stop the previous container.
        self.stop()

        # Start a new container.
        self.start()

    def _get_base_args(self):
        return [
            'docker', 'run',
            '-d', '--rm',
            '--name', DOCKER_CONTAINER_NAME,
            '-v', '/var/run/docker.sock:/var/run/docker.sock',
            '-v', '/tmp/autograder-temp/:/tmp/autograder-temp',
            '-p', '%d:%d' % (self._port, DEFAULT_PORT),
            self._image,
        ]

    def _pull_image(self, **kwargs):
        print("Pulling Latest Image ...")
        util.run(['docker', 'pull', self._image])
        print("Pulling Complete")

class SourceServer(BaseServer):
    def __init__(self, source_dir = None, **kwargs):
        super().__init__(**kwargs)

        self._source_dir = source_dir
        self._process = None

        if (self._source_dir is None):
            raise ValueError("No source dir provided.")

        if (not os.path.isdir(self._source_dir)):
            raise ValueError("Source dir does not exist or is not a dir: '%s'." % (self._source_dir))

        # Before starting the server the first time,
        # try to build the server so future starts are faster.
        self._prebuild()

        # Try to stop the server on termination.
        atexit.register(self.stop)

    def start(self, **kwargs):
        if (self._process is not None):
            raise ValueError("A server is already running, cannot start a new one.")

        args = self._get_base_args()
        self._process = util.run_in_background(args, cwd = self._source_dir)

        status = None
        try:
            # Ensure the server is running cleanly.
            status = self._process.wait(SOURCE_START_SLEEP_TIME_SECS)
        except subprocess.TimeoutExpired:
            # Good, the server is running.
            pass

        if (status is not None):
            raise ValueError("Server was unable to start successfully (code: '%s')." % (str(status)))

    def stop(self, **kwargs):
        if (self._process is None):
            return

        status = self._process.poll()
        if (status is not None):
            return

        # Try to end the server gracefully.
        self._process.send_signal(signal.SIGINT)

        try:
            self._process.wait(SOURCE_KILL_SLEEP_TIME_SECS)
        except subprocess.TimeoutExpired:
            # End the server hard.
            self._process.kill()
            time.sleep(SOURCE_KILL_SLEEP_TIME_SECS)

        self._process = None

    def reset(self, **kwargs):
        # Stop the previous server.
        self.stop()

        # Start a new server.
        self.start()

    def _get_base_args(self):
        return [
            './bin/server',
            '-c', 'web.port=%d' % (self._port),
            '--log-level', 'ERROR',
            '--unit-testing',
        ]

    def _prebuild(self, **kwargs):
        args = [
            './scripts/build.sh', 'server',
        ]

        util.run(args, cwd = self._source_dir)
