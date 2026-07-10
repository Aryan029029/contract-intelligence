import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import google.generativeai as genai

from config.settings import GEMINI_API_KEY, MODEL_NAME

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)


def generate_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text.strip()