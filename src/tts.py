# Text-to-speech module
"""
tts.py
---------------------------------------
Text-to-Speech module for Smart Blind Cane OCR.

Responsibilities:
    1. Initialize text-to-speech engine
    2. Configure voice, rate and volume
    3. Convert OCR text into speech
    4. Stop speech when required
"""

import pyttsx3

from src.config import (
    VOICE_RATE,
    VOICE_VOLUME,
    VOICE_ID,
)

from src.logger import logger
from src.exceptions import SpeechError


class TextToSpeech:
    """
    Handles offline text-to-speech using pyttsx3.
    """

    def __init__(self) -> None:

        try:

            logger.info(
                "Initializing Text-to-Speech..."
            )

            self.engine = pyttsx3.init()

            # --------------------------------------------------
            # Speech Rate
            # --------------------------------------------------

            self.engine.setProperty(
                "rate",
                VOICE_RATE
            )

            # --------------------------------------------------
            # Volume
            # --------------------------------------------------

            self.engine.setProperty(
                "volume",
                VOICE_VOLUME
            )

            # --------------------------------------------------
            # Voice
            # --------------------------------------------------

            voices = self.engine.getProperty(
                "voices"
            )

            if voices:

                if 0 <= VOICE_ID < len(voices):

                    self.engine.setProperty(
                        "voice",
                        voices[VOICE_ID].id
                    )

            logger.info(
                "Text-to-Speech initialized successfully."
            )

        except Exception as error:

            logger.exception(
                "Failed to initialize Text-to-Speech."
            )

            raise SpeechError(
                f"TTS initialization failed: {error}"
            ) from error

    # ==========================================================
    # SPEAK
    # ==========================================================

    def speak(self, text: str) -> None:
        """
        Speak the supplied text.
        """

        if not text or not text.strip():

            logger.warning(
                "No text provided for speech."
            )

            return

        try:

            text = text.strip()

            logger.info(
                f"Speaking text: {text}"
            )

            self.engine.say(text)

            self.engine.runAndWait()

            logger.info(
                "Speech completed."
            )

        except Exception as error:

            logger.exception(
                "Text-to-Speech failed."
            )

            raise SpeechError(
                f"Speech failed: {error}"
            ) from error

    # ==========================================================
    # STOP
    # ==========================================================

    def stop(self) -> None:
        """
        Stop current speech.
        """

        try:

            self.engine.stop()

            logger.info(
                "Speech stopped."
            )

        except Exception as error:

            logger.exception(
                "Failed to stop speech."
            )

    # ==========================================================
    # GET VOICES
    # ==========================================================

    def get_voices(self) -> list:
        """
        Return all voices installed on the system.
        """

        try:

            voices = self.engine.getProperty(
                "voices"
            )

            return voices

        except Exception as error:

            logger.exception(
                "Could not retrieve voices."
            )

            return []


# ==============================================================
# STANDALONE TEST
# ==============================================================

if __name__ == "__main__":

    print("=" * 50)
    print("SMART BLIND CANE - TTS TEST")
    print("=" * 50)

    try:

        tts = TextToSpeech()

        test_text = (
            "Hello. "
            "This is the Smart Blind Cane "
            "text to speech system."
        )

        print(
            f"\nSpeaking:\n{test_text}\n"
        )

        tts.speak(test_text)

        print(
            "\nSpeech test completed."
        )

    except SpeechError as error:

        print(
            f"\nSpeech Error: {error}"
        )