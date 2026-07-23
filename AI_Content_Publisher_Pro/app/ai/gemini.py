from google import genai
from google.genai.errors import ClientError, ServerError

from app.core.config import settings
from app.ai.providers.base import BaseProvider


class GeminiProvider(BaseProvider):

    MODELS = [
        "gemini-flash-latest",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite",
    ]

    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_key)

    def generate(self, prompt: str) -> str:
        last_error = None

        for model in self.MODELS:
            try:
                print(f"Используем модель: {model}")

                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                return response.text

            except (ClientError, ServerError) as e:
                print(f"{model} недоступна: {e}")
                last_error = e

        raise RuntimeError(f"Все модели недоступны.\n{last_error}")