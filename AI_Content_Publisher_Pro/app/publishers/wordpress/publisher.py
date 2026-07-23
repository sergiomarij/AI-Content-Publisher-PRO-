import json
from pathlib import Path

from app.publishers.wordpress.client import WordPressClient
from app.publishers.wordpress.config import WordPressConfig


class WordPressPublisher:

    def _get_last_article(self):

        outputs = sorted(Path("outputs").glob("ART-*"))

        if not outputs:
            return None, None, None

        last = outputs[-1]

        article = last / "article.md"

        meta = last / "meta.json"

        if not article.exists() or not meta.exists():
            return None, None, None

        with open(meta, encoding="utf-8") as f:
            title = json.load(f)["title"]

        with open(article, encoding="utf-8") as f:
            content = f.read()

        return title, content, last

    def publish_last(self, status="publish"):

        cfg = WordPressConfig().load()

        client = WordPressClient(
            cfg["url"],
            cfg["username"],
            cfg["application_password"]
        )

        title, content, folder = self._get_last_article()

        if title is None:
            return False, "Нет статей."

        response = client.publish(
            title=title,
            content=content,
            status=status
        )

        if response.status_code in (200, 201):
            if status == "draft":
                return True, "Черновик создан."
            return True, "Статья опубликована."

        return False, response.text

    def list_categories(self):

        cfg = WordPressConfig().load()

        client = WordPressClient(
            cfg["url"],
            cfg["username"],
            cfg["application_password"]
        )

        response = client.get_categories()

        if response.status_code != 200:
            return False, response.text

        categories = response.json()

        return True, categories

    def list_tags(self):

        cfg = WordPressConfig().load()

        client = WordPressClient(
            cfg["url"],
            cfg["username"],
            cfg["application_password"]
        )

        response = client.get_tags()

        if response.status_code != 200:
            return False, response.text

        tags = response.json()

        return True, tags
