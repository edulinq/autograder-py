class AutograderError(Exception):
    pass

class APIError(AutograderError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code

class ConnectionError(AutograderError):
    pass
