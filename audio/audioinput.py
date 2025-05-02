from logging import getLogger
import speech_recognition as sr

from audio.audiodevicemanagement import AudioDeviceManager


class SpeechCollector:
    """Class responsible for collecting audio input from the microphone and processing it to recognize user speech."""
    
    __slots__ = ('_audio_device_manager', '_logger', '_microphone', '_speech_recognizer')

    def __init__(self, audio_device_manager: AudioDeviceManager):
        self._logger = getLogger(self.__class__.__name__)
        self._audio_device_manager = audio_device_manager
        self._initialize_microphone()

    def _initialize_microphone(self):
        try:
            self._microphone = sr.Microphone(device_index=self._audio_device_manager.get_input_device().get('index'))
            assert self._microphone, "Microphone not found."
            self._speech_recognizer = sr.Recognizer()
        except Exception as e:
            self._logger.error(f"Error initializing microphone: {e}", exc_info=True)
            raise

    def capture_speech(self) -> str:
        with self._microphone as source:
            self._logger.info("Listening for speech...")
            self._speech_recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self._speech_recognizer.listen(source)
            self._logger.info("Audio captured, processing...")
            try:
                text = self._speech_recognizer.recognize_google(audio)
                self._logger.info(f"Recognized speech: {text}")
                return text
            except sr.UnknownValueError:
                self._logger.error("Could not understand the audio.")
                return ""
            except sr.RequestError as e:
                self._logger.error(f"Could not request results; {e}")
                return ""
