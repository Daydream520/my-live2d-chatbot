from src.agents.llm_agent import LLMAgent
from src.logger_config import logger


class Orchestrator:
    def __init__(self):
        """
        Initializes the Orchestrator, which manages the interaction between different agents.
        """
        self.llm_agent = LLMAgent()
        self.logger = logger
        self.logger.info("Orchestrator initialized.")

    def run_text_interaction(self):
        """
        Runs a console-based text interaction loop.
        """
        self.logger.info("Starting text interaction loop.")
        print("Welcome to the MyLive2DChatbot!")
        print("You can start chatting. Type 'quit' to exit.")

        while True:
            try:
                user_input = input("You: ")

                if user_input.lower() == "quit":
                    self.logger.info("User requested to quit the application.")
                    print("Goodbye!")
                    break

                agent_response = self.llm_agent.generate_response(user_input)
                print(f"Agent: {agent_response}")

            except KeyboardInterrupt:
                self.logger.info("Application interrupted by user (Ctrl+C).")
                print("\nGoodbye!")
                break
            except Exception as e:
                self.logger.error(f"An unexpected error occurred: {e}", exc_info=True)
                print("An unexpected error occurred. Please check the logs. Exiting.")
                break

        self.logger.info("Text interaction loop finished.")
