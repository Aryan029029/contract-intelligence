import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from google import genai

from config.settings import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(prompt: str) -> str:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text