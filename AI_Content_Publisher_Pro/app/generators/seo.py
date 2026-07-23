from app.ai.manager import AIManager
from app.ai.prompts import SEO_PROMPT


class SEOGenerator:

    def __init__(self):
        self.ai = AIManager()

    def generate(self, topic: str):

        prompt = SEO_PROMPT.format(topic=topic)

        return self.ai.generate(prompt)