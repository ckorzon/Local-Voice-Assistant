from json import loads
from requests import Response


class AiResponse:

    __slots__ = ("_raw_response", "_response_chunks_iter", "_done")

    def __init__(self, response: Response):
        self._raw_response = response
        self._response_chunks_iter = None
        self._done = False

    def __iter__(self):
        # Set any necessary state for iteration
        self._response_chunks_iter = self._raw_response.iter_content()
        self._done = False
        return self

    def __next__(self):
        if self._done:
            raise StopIteration
        current_chunk = ""
        while not current_chunk.endswith("\n"):
            chunk = next(self._response_chunks_iter, None)
            if not chunk:
                self._done = True
                break
            chunk_str = chunk.decode("utf-8")
            current_chunk += chunk_str
        chunk_json = loads(current_chunk)
        if chunk_json.get("done"):
            self._done = True
        return chunk_json.get("response")
        
