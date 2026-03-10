from openai import OpenAI
from app.core.config import OPENAI_API_KEY

def get_client():
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not set.")
    return OpenAI(api_key=OPENAI_API_KEY)