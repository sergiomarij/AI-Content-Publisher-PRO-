from app.ai.manager import AIManager
from app.ai.prompts import REVIEW_PROMPT


class ReviewGenerator:
    def __init__(self):
        self.ai = AIManager()

    def generate(self, topic: str) -> str:
        return self.ai.generate(REVIEW_PROMPT.format(topic=topic))
