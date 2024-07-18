class APIError(Exception):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)
