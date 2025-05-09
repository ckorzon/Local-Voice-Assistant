
from typing import Iterator
from chatbot.aiconfig import AIConfig
from chatbot.airesponse import AiResponse
from lva_http.httpclient import HttpClient

PROMPT_TEMPLATE = """\
You are a helpful assistant, and your name is {name}.
Your task is to assist the user with their questions and provide accurate information.
The user may ask you anything, and you should respond to the best of your ability.
Please remember to be polite and helpful at all times.
"""

class AiClient:

    __slots__ = ("_model", "_name", "_http_client")

    def __init__(self, ai_config: AIConfig):
        self._model = ai_config.model
        self._name = ai_config.name
        self._http_client = HttpClient(ai_config.endpoint)

    def initialize_session(self):
        self.get_response_for_prompt(PROMPT_TEMPLATE.format(name=self._name))

    def get_response_for_prompt(self, prompt: str) -> AiResponse:
        data = {
            "model": self._model,
            "prompt": prompt
        }
        response = self._http_client.post_request("api/generate", data=data)
        return AiResponse(response)

