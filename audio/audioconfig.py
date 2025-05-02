class AudioConfig:
    """Simple class to hold audio configuration settings."""    


    __slots__ = ("preferred_api", "input_device_name", "output_device_name")


    def __init__(self, preferred_api: str, input_device_name: str, output_device_name: str):
        self.preferred_api = preferred_api
        self.input_device_name = input_device_name
        self.output_device_name = output_device_name

    @staticmethod
    def from_dict(config_dict: dict):
        """Creates an AudioConfig instance from a dictionary."""
        return AudioConfig(
            preferred_api=config_dict.get("preferred_api"),
            input_device_name=config_dict.get("input_device"),
            output_device_name=config_dict.get("output_device")
        )

