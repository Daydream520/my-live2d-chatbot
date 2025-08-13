import os
from dotenv import load_dotenv

# Load environment variables from a .env file at the project root.
# find_dotenv() will search for the .env file in parent directories.
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
