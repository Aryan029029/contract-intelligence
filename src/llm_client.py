import time
import random

from groq import Groq

from config.settings import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)


def generate_response(prompt: str) -> str:

    wait_time = 3

    for attempt in range(5):

        try:

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0,
            )

            return response.choices[0].message.content or ""

        except Exception as e:

            error = str(e)

            if (
                "429" in error
                or "rate" in error.lower()
                or "limit" in error.lower()
            ):

                jitter = random.uniform(0, 2)

                print(
                    f"\nRate limit hit."
                    f"\nRetry {attempt + 1}/5"
                    f"\nWaiting {wait_time + jitter:.1f} seconds..."
                )

                time.sleep(wait_time + jitter)

                wait_time *= 2

                continue

            raise

    raise Exception(
        "Groq API is currently unavailable. Please try again in a few minutes."
    )