class AuthorizeException(Exception):
    def __init__(self, detail: str):
        self.detail = detail


class AuthorizeTemplateException(Exception):
    def __init__(self, detail: str):
        self.detail = detail
