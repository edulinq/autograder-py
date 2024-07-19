import http
import http.server
import json
import multiprocessing
import time
import urllib.parse

import autograder.api.constants
import autograder.util.timestamp

PORT = 12345
ENCODING = 'utf8'

SLEEP_TIME_SEC = 0.2
REAP_TIME_SEC = 0.5

def start():
    next_response_queue = multiprocessing.Queue()

    process = multiprocessing.Process(target = _run, args = (next_response_queue,))
    process.start()

    time.sleep(SLEEP_TIME_SEC)

    return process, next_response_queue

def stop(process):
    if (process.is_alive()):
        process.terminate()
        process.join(REAP_TIME_SEC)

        if (process.is_alive()):
            process.kill()
            process.join(REAP_TIME_SEC)

    process.close()

def _run(next_response_queue):
    Handler._next_response_queue = next_response_queue
    server = http.server.HTTPServer(('', PORT), Handler)
    server.serve_forever()

class Handler(http.server.BaseHTTPRequestHandler):
    _next_response_queue = None

    def log_message(self, format, *args):
        return

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        raw_content = self.rfile.read(length).decode(ENCODING)
        content = urllib.parse.parse_qs(raw_content)

        data = content[autograder.api.constants.API_REQUEST_JSON_KEY][0]

        headers = {}
        content = Handler._next_response_queue.get()
        message = content.get('message', "")
        code = content.get('code', http.HTTPStatus.OK)

        now = autograder.util.timestamp.get()

        data = {
            "id": "00000000-0000-0000-0000-000000000000",
            "locator": "",
            "server-version": "0.0.0",
            "start-timestamp": now,
            "end-timestamp": now,
            "status": code,
            autograder.api.constants.API_RESPONSE_KEY_SUCCESS: (code == http.HTTPStatus.OK),
            autograder.api.constants.API_RESPONSE_KEY_MESSAGE: message,
            autograder.api.constants.API_RESPONSE_KEY_CONTENT: content,
        }

        payload = json.dumps(data)

        self.send_response(code)

        for (key, value) in headers:
            self.send_header(key, value)
        self.end_headers()

        self.wfile.write(payload.encode(ENCODING))
