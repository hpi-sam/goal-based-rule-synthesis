import os
import time
import requests
from pathlib import Path
from utils.logger import get_logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logger
logger = get_logger()

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set in .env file")

def call_llm(prompt: str, max_tokens: int = 512, temperature: float = 0.0) -> str:
    """
    Call OpenAI API with retries and return the generated text.
    """
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": OPENAI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    for attempt in range(3):
        try:
            logger.info(f"Calling OpenAI (attempt {attempt+1}) with prompt: {prompt[100]}...")
            resp = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            resp.raise_for_status()
            text = resp.json()["choices"][0]["message"]["content"]
            logger.info(f"Received response: {text}...")
            return text

        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as e:
            logger.warning(f"Timeout on attempt {attempt+1}, retrying... Error: {e}")
            time.sleep(2)

    raise RuntimeError("OpenAI API failed after 3 retries")

