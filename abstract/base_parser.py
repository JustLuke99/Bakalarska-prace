class BaseParser:
    supported_languages: list = []

    def __init__(self):
        self.return_data = None

    def get_languages(self):
        raise NotImplementedError

    def parse(self, **kwargs):
        raise NotImplementedError
