import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URL for the FastAPI backend
# Default to localhost if not specified in environment
BASE_API_URL = os.getenv("BASE_API_URL", "http://localhost:8000")

# Default headers for API requests
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# API Timeout settings (in seconds)
API_TIMEOUT = 10.0
