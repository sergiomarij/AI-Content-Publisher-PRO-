from pathlib import Path


class ArticleViewer:

    def open(self, article):

        folder = Path(article["folder"])

        file = folder / "article.md"

        if not file.exists():
            return "Статья не найдена."

        with open(file, "r", encoding="utf-8") as f:
            return f.read()
