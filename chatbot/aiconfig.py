
class AIConfig:

    __slots__ = ("model", "name", "endpoint")

    def __init__(self, model: str, name: str, endpoint: str):
        self.model = model
        self.name = name
        self.endpoint = endpoint

    @staticmethod
    def from_dict(config: dict) -> "AIConfig":
        return AIConfig(
            model=config.get("model"),
            name=config.get("name"),
            endpoint=config.get("endpoint")
        )
