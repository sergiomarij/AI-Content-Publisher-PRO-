from app.ai.manager import AIManager
from app.ai.prompts import REWRITE_PROMPT


class RewriteGenerator:
    def __init__(self):
        self.ai = AIManager()

    def generate(self, text: str) -> str:
        return self.ai.generate(REWRITE_PROMPT.format(text=text))
