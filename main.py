from yaml import safe_load
import logging

from audio.audioconfig import AudioConfig
from audio.audiodevicemanagement import AudioDeviceManager
from audio.audioinput import SpeechCollector
from chatbot.aiclient import AiClient
from chatbot.aiconfig import AIConfig


CONFIG = safe_load(open('config.yaml', 'r', encoding='utf-8'))
assert CONFIG, "Configuration file not found or empty."
print(CONFIG)

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S %z"
logging.basicConfig(level=logging.INFO, filename=CONFIG.get("log_file"), filemode="w", format="%(asctime)s|%(levelname)s|%(name)s|%(message)s", datefmt=TIMESTAMP_FORMAT)
LOGGER = logging.getLogger("Main")


def main():
    LOGGER.info("Setting up local voice assistant...")
    # Setup Audio
    assert CONFIG.get("audio"), "Audio configuration not found."
    audio_config = AudioConfig.from_dict(CONFIG.get("audio"))
    audio_device_manager = AudioDeviceManager(audio_config)
    speech_collector = SpeechCollector(audio_device_manager)
    # Setup AI Chatbot
    assert CONFIG.get("ai_config"), "AI configuration not found."
    ai_config = AIConfig.from_dict(CONFIG.get("ai_config"))
    ai_chatbot = AiClient(ai_config)
    # Run Program
    LOGGER.info("Now listening for speech...")
    while True:
        speech_captured = speech_collector.capture_speech()
        LOGGER.info(f"Captured speech: {speech_captured}")
        ai_response = ai_chatbot.get_response_for_prompt(speech_captured)
        LOGGER.info("AI Response:")
        for line in ai_response:
            print(line, end="")
        print()



if __name__ == "__main__":
    main()
