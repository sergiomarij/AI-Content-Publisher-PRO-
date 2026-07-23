from pathlib import Path

from app.publishers.wordpress.client import WordPressClient
from app.publishers.wordpress.config import WordPressConfig


class WordPressPublisher:

    def publish_last(self):

        cfg = WordPressConfig().load()

        client = WordPressClient(
            cfg["url"],
            cfg["username"],
            cfg["application_password"]
        )

        outputs = sorted(Path("outputs").glob("ART-*"))

        if not outputs:
            return False, "Нет статей."

        last = outputs[-1]

        article = last / "article.md"

        meta = last / "meta.json"

        if not article.exists():
            return False, "Файл article.md отсутствует."

        import json

        with open(meta, encoding="utf-8") as f:
            title = json.load(f)["title"]

        with open(article, encoding="utf-8") as f:
            content = f.read()

        response = client.publish(
            title=title,
            content=content,
            status="publish"
        )

        if response.status_code in (200, 201):
            return True, "Статья опубликована."

        return False, response.text