import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY")
