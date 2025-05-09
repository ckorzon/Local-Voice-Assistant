
class AIConfig:

    __slots__ = ("model", "name", "endpoint")

    def __init__(self, model: str, name: str, endpoint: str):
        self.model = model
        self.name = name
        self.endpoint = endpoint

