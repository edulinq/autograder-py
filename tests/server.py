import http
import http.server
import multiprocessing
import time
import urllib.parse

PORT = 12345
ENCODING = 'utf8'
POST_CONTENT_KEY = 'content'

SLEEP_TIME_SEC = 0.5
REAP_TIME_SEC = 1

def start():
    process = multiprocessing.Process(target = _run)
    process.start()

    time.sleep(SLEEP_TIME_SEC)

    return process

def stop(process):
    if (process.is_alive()):
        process.terminate()
        process.join(REAP_TIME_SEC)

        if (process.is_alive()):
            process.kill()
            process.join(REAP_TIME_SEC)

    process.close()

def _run():
    server = http.server.HTTPServer(('', PORT), Handler)
    server.serve_forever()

class Handler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        raw_content = self.rfile.read(length).decode(ENCODING)
        content = urllib.parse.parse_qs(raw_content)

        data = content[POST_CONTENT_KEY][0]

        code, headers, payload = self._route(self.path, data)

        self.send_response(code)

        for (key, value) in headers:
            self.send_header(key, value)
        self.end_headers()

        self.wfile.write(payload.encode(ENCODING))

    def _route(self, path, data):
        """
        Returns: (code, headers, payload)
        """

        if (path == '/api/v01/peek'):
            return self._handle_peek(data)
        elif (path == '/api/v01/history'):
            return self._handle_history(data)
        else:
            return http.HTTPStatus.NOT_FOUND, {}, ''

    def _handle_peek(self, data):
        payload = """{
            "success": true,
            "status": 200,
            "timestamp": "2023-09-30T11:47:27.841645832-07:00",
            "content": {
                "result": {
                    "name": "HW0",
                    "questions": [
                        {
                            "name": "Q1",
                            "max_points": 1,
                            "score": 1,
                            "message": ""
                        },
                        {
                            "name": "Q2",
                            "max_points": 1,
                            "score": 1,
                            "message": ""
                        },
                        {
                            "name": "Style",
                            "max_points": 0,
                            "score": 0,
                            "message": "Style is clean!"
                        }
                    ]
                }
            }
        }"""

        return http.HTTPStatus.OK, {}, payload

    def _handle_history(self, data):
        payload = """{
            "success": true,
            "status": 200,
            "timestamp": "2023-09-30T12:22:41.091853098-07:00",
            "content": {
                "history": [
                    {
                        "id": "COURSE101::hw0::user@test.com::1",
                        "message": "",
                        "max_points": 2,
                        "score": 1,
                        "grading_start_time": "2023-09-25T22:50:54.225052Z"
                    },
                    {
                        "id": "COURSE101::hw0::user@test.com::2",
                        "message": "",
                        "max_points": 2,
                        "score": 1,
                        "grading_start_time": "2023-09-25T22:51:54.225052Z"
                    }
                ]
            }
        }"""

        return http.HTTPStatus.OK, {}, payload
