from app.core.config import settings
from app.ai.gemini import GeminiProvider


class AIManager:
    def __init__(self):
        provider = settings.provider.lower()

        if provider == "gemini":
            self.provider = GeminiProvider()
        else:
            raise ValueError(f"Неизвестный провайдер: {provider}")

    def generate(self, prompt: str) -> str:
        return self.provider.generate(prompt)