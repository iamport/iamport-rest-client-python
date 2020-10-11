class ResponseError(Exception):
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message

class HttpError(Exception):
    def __init__(self, code=None, reason=None):
        self.code = code
        self.reason = reason

class NeedEssentialParameterException(Exception):
    def __init__(self, key):
        self.message = 'Essential parameter is missing!: {}'.format(key)

    def __str__(self):
        return self.message

