from app.ai.manager import AIManager
from app.ai.prompts import NEWS_PROMPT


class NewsGenerator:
    def __init__(self):
        self.ai = AIManager()

    def generate(self, topic: str) -> str:
        return self.ai.generate(NEWS_PROMPT.format(topic=topic))
