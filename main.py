from src.orchestrator import Orchestrator
from src.logger_config import logger


def main():
    """
    Main function to initialize and run the application.
    """
    logger.info("Application starting up.")
    try:
        app = Orchestrator()
        app.run_text_interaction()
    except Exception as e:
        logger.critical(
            f"A fatal error occurred in the main application loop: {e}", exc_info=True
        )
        print("A fatal error occurred. Please check the logs for details.")
    finally:
        logger.info("Application shutting down.")


if __name__ == "__main__":
    main()
