from app.ai.manager import AIManager
from app.ai.prompts import TELEGRAM_PROMPT


class TelegramGenerator:
    def __init__(self):
        self.ai = AIManager()

    def generate(self, topic: str) -> str:
        return self.ai.generate(TELEGRAM_PROMPT.format(topic=topic))
