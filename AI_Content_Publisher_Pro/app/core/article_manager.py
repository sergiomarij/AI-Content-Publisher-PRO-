from pathlib import Path
from datetime import datetime
import json


OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


class ArticleManager:

    def create_article(self, title: str):

        article_id = datetime.now().strftime("ART-%Y%m%d-%H%M%S")

        folder = OUTPUT_DIR / article_id
        folder.mkdir(exist_ok=True)

        meta = {
            "id": article_id,
            "title": title,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "generated",
        }

        with open(folder / "meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4, ensure_ascii=False)

        return article_id, folder

    def save_markdown(self, folder: Path, article: str):

        with open(folder / "article.md", "w", encoding="utf-8") as f:
            f.write(article)

    def save_html(self, folder: Path, article: str):

        html = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>AI Content Publisher PRO</title>
</head>

<body>

<pre>

{article}

</pre>

</body>
</html>
"""

        with open(folder / "article.html", "w", encoding="utf-8") as f:
            f.write(html)

    def save_text(self, folder: Path, article: str):

        with open(folder / "article.txt", "w", encoding="utf-8") as f:
            f.write(article)