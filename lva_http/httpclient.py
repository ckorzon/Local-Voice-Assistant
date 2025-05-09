
from logging import getLogger
from requests import Session

class HttpClient:

    __slots__ = ('_session', '_base_url', '_logger', '_fixed_headers')

    def __init__(self, base_url: str):
        self._base_url = base_url
        self._session = Session()
        self._logger = getLogger(self.__class__.__name__)
        self._fixed_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def post_request(self, route: str, headers: dict = None, data: dict = None, stream: bool = False) -> dict:
        url = f"{self._base_url}/{route}"
        request_headers = self._fixed_headers.copy()
        if headers:
            request_headers.update(headers)
        self._logger.debug(f"Sending POST request to {url} with headers {headers} and data {data}")
        response = self._session.post(url, headers=headers, json=data, stream=stream)
        response.raise_for_status()
        return response.json()

    def get_request(self, route: str, headers: dict = None, stream: bool = False) -> dict:
        url = f"{self._base_url}/{route}"
        request_headers = self._fixed_headers.copy()
        if headers:
            request_headers.update(headers)
        self._logger.debug(f"Sending GET request to {url} with headers {headers}")
        response = self._session.get(url, headers=headers, stream=stream)
        response.raise_for_status()
        return response.json()
