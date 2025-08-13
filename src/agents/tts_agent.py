import os
import tempfile
import pygame
from gtts import gTTS
import threading
import time
from src.logger_config import logger

class TTSAgent:
    def __init__(self):
        """
        Initializes the TTSAgent. It tries to initialize the pygame mixer,
        but will not crash if no audio device is found.
        """
        self.mixer_initialized = False
        try:
            pygame.mixer.init()
            self.mixer_initialized = True
            logger.info("TTSAgent initialized and pygame mixer started.")
        except pygame.error as e:
            logger.warning(f"Could not initialize pygame mixer: {e}. TTS audio will not be played.")

    def speak(self, text: str):
        """
        Generates speech from text and plays it without blocking.
        It launches a background thread to handle the cleanup of the
        temporary audio file after playback is complete.

        Args:
            text (str): The text to be spoken.
        """
        if not self.mixer_initialized:
            logger.warning(f"Mixer not initialized. Cannot play text: '{text}'")
            return

        try:
            # Using delete=False and manually handling cleanup is necessary
            # for the file to persist long enough for playback.
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            temp_filename = temp_file.name
            temp_file.close()  # Close the file handle so gTTS can write to it

            # Generate speech and save to the temp file
            tts = gTTS(text=text, lang='zh-tw')
            tts.save(temp_filename)
            logger.info(f"Generated TTS audio and saved to {temp_filename}")

            # Load and play the audio
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            logger.info(f"Started playing TTS audio for text: '{text}'")

            # Start a daemon thread to clean up the file after playback
            cleanup_thread = threading.Thread(target=self._cleanup_task, args=(temp_filename,))
            cleanup_thread.daemon = True
            cleanup_thread.start()

        except Exception as e:
            logger.error(f"Error in TTS speak method: {e}")

    def _cleanup_task(self, filepath: str):
        """
        Awaits the end of playback and then deletes the audio file.
        This method is intended to be run in a separate thread.
        """
        # Poll until the music is no longer busy
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        # Unload the music to release any file lock, especially on Windows
        pygame.mixer.music.unload()

        # A small delay to ensure the file system has released the file
        time.sleep(0.1)

        try:
            os.unlink(filepath)
            logger.info(f"Cleaned up temporary file: {filepath}")
        except OSError as e:
            logger.error(f"Error deleting temp file {filepath}: {e}")

    def is_busy(self) -> bool:
        """
        Checks if the pygame mixer is currently busy playing audio.

        Returns:
            bool: True if audio is playing, False otherwise.
        """
        if not self.mixer_initialized:
            return False
        return pygame.mixer.music.get_busy()
