from pyaudio import PyAudio
from yaml import safe_load
from time import sleep
import speech_recognition as sr
from logging import getLogger
from audio.audioconfig import AudioConfig


class AudioDeviceManager:

    __slots__ = ('_api_info', '_api_index', '_audio_handler', '_input_device', '_logger', '_output_device')

    def __init__(self, audio_config: AudioConfig):
        self._logger = getLogger(self.__class__.__name__)
        self._audio_handler = PyAudio()
        self._find_audio_api(audio_config.preferred_api)
        self._acquire_input_device(audio_config.input_device_name)
        self._acquire_output_device(audio_config.output_device_name)

    def _find_audio_api(self, target_api_name: str):
        """Attempts to find the underlying OS audio API info for the given target_api_name.
        If the API is not found, throws an AssertionError.

        Args:
            target_api_name (str): The name of the host audio API to search for. Example: "ALSA", "Windows WASAPI", etc.

        Returns:
            None
        """
        try:
            api_info, api_index = None, 0
            for i in range(self._audio_handler.get_host_api_count()):
                api_info = self._audio_handler.get_host_api_info_by_index(i)
                if api_info.get('name') == target_api_name:
                    api_index = i
                    break
            self._api_info = api_info
            self._api_index = api_index
            assert self._api_info, f"Audio API '{target_api_name}' not found."
        except Exception as e:
            self._logger.error(f"Error finding audio API: {e}", exc_info=True)
            raise

    def _acquire_input_device(self, device_name: str):
        try:
            self._input_device = self._find_audio_device(device_name)
            assert self._input_device, f"Input device '{device_name}' not found."
        except Exception as e:
            self._logger.error(f"Error acquiring input device: {e}", exc_info=True)
            raise

    def _acquire_output_device(self, device_name: str):
        try:
            self._output_device = self._find_audio_device(device_name)
            assert self._output_device, f"Output device '{device_name}' not found."
        except Exception as e:
            self._logger.error(f"Error acquiring output device: {e}", exc_info=True)
            raise

    def _find_audio_device(self, device_name: str):
        """Attempts to find and return the PyAudio device info for the given device_name.
        If the device is not found, returns None.

        Args:
            device_name (str): _description_

        Returns:
            _PaDeviceInfo: PyAudio device info object for the targeted audio device.
        """
        device_name = device_name.upper()
        host_info = self._audio_handler.get_host_api_info_by_index(self._api_index)
        num_devices = host_info.get('deviceCount')
        audio_device = None
        for i in range(0, num_devices):
            device_info = self._audio_handler.get_device_info_by_host_api_device_index(self._api_index, i)
            if device_info.get('name').upper() == device_name:
                audio_device = device_info
        return audio_device

    def get_input_device(self):
        """Returns the input device info."""
        return self._input_device
    
    def get_output_device(self):
        """Returns the output device info."""
        return self._output_device

    def __del__(self):
        """Destructor to clean up the audio handler."""
        if self._audio_handler:
            self._audio_handler.terminate()
            self._logger.info("Audio handler terminated.")
