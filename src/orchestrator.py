import pygame
from src.agents.llm_agent import LLMAgent
from src.agents.tts_agent import TTSAgent
from src.logger_config import logger


class Orchestrator:
    def __init__(self):
        """
        Initializes the Orchestrator, which manages the interaction between different agents.
        """
        self.llm_agent = LLMAgent()
        self.tts_agent = TTSAgent()
        self.logger = logger
        self.logger.info("Orchestrator initialized.")

    def run_text_interaction(self):
        """
        Runs a console-based text interaction loop, including TTS for the agent's responses.
        """
        self.logger.info("Starting text interaction loop.")
        print("Welcome to the MyLive2DChatbot!")
        print("You can start chatting. Type 'quit' to exit.")

        # Initialize pygame clock for controlling the loop speed
        clock = pygame.time.Clock()

        while True:
            try:
                user_input = input("You: ")

                if user_input.lower() == "quit":
                    self.logger.info("User requested to quit the application.")
                    print("Goodbye!")
                    break

                response_text = self.llm_agent.generate_response(user_input)
                print(f"Chatbot: {response_text}")

                # Speak the response and wait for it to finish
                self.tts_agent.speak(response_text)
                while self.tts_agent.is_busy():
                    clock.tick(10)  # Wait, polling 10 times per second

            except KeyboardInterrupt:
                self.logger.info("Application interrupted by user (Ctrl+C).")
                print("\nGoodbye!")
                break
            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
                print("An unexpected error occurred. Please check the logs. Exiting.")
                break

        self.logger.info("Text interaction loop finished.")
