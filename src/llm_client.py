import time

from google import genai
from config.settings import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_response(prompt: str) -> str:
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            return response.text

        except Exception as e:
            error = str(e)

            if "429" in error or "RESOURCE_EXHAUSTED" in error:
                wait_time = 30
                print(f"Rate limit hit. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            raise

    raise Exception("Failed after multiple retries.")