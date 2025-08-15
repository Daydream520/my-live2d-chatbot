import google.generativeai as genai
from src.config import OPENAI_API_KEY, GOOGLE_API_KEY
from src.logger_config import logger


class LLMAgent:
    def __init__(self):
        """
        Initializes the LLMAgent, loading API keys, configuring the Google
        Generative AI model, and the logger.
        """
        self.openai_api_key = OPENAI_API_KEY
        self.google_api_key = GOOGLE_API_KEY
        self.logger = logger

        self.logger.info("LLMAgent initialized.")
        if not self.google_api_key:
            self.logger.warning(
                "GOOGLE_API_KEY is missing. The agent may not function correctly."
            )
        else:
            genai.configure(api_key=self.google_api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash-latest")
            self.logger.info("Google Generative AI model initialized.")

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response using the Google Gemini model.

        Args:
            prompt (str): The input prompt from the user.

        Returns:
            str: The generated response text.
        """
        self.logger.info(f"Sending prompt to Gemini: '{prompt}'")
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            self.logger.info(f"Received response from Gemini: '{response_text}'")
            return response_text
        except Exception as e:
            self.logger.error(f"Error generating response from Gemini: {e}")
            return "Sorry, I encountered an error while generating a response."
