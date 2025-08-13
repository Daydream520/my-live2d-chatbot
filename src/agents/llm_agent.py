from src.config import OPENAI_API_KEY, GOOGLE_API_KEY
from src.logger_config import logger


class LLMAgent:
    def __init__(self):
        """
        Initializes the LLMAgent, loading API keys and the logger.
        """
        self.openai_api_key = OPENAI_API_KEY
        self.google_api_key = GOOGLE_API_KEY
        self.logger = logger

        self.logger.info("LLMAgent initialized.")
        if not self.openai_api_key or not self.google_api_key:
            self.logger.warning(
                "One or both API keys are missing. The agent may not function correctly."
            )

    def generate_response(self, prompt: str) -> str:
        """
        A placeholder method to generate a response.

        Args:
            prompt (str): The input prompt from the user.

        Returns:
            str: A fixed response string.
        """
        self.logger.info(f"LLMAgent received prompt: '{prompt}'")
        response = "Response from LLM Agent"
        self.logger.info(f"LLMAgent generated response: '{response}'")
        return response
