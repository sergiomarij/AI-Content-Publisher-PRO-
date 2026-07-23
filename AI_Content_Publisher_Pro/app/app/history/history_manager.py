from pathlib import Path
import json

OUTPUT_DIR = Path("outputs")


class HistoryManager:

    def get_articles(self):

        if not OUTPUT_DIR.exists():
            return []

        articles = []

        for folder in sorted(OUTPUT_DIR.iterdir(), reverse=True):

            if not folder.is_dir():
                continue

            meta = folder / "meta.json"

            if not meta.exists():
                continue

            with open(meta, "r", encoding="utf-8") as f:
                data = json.load(f)

            data["folder"] = folder

            articles.append(data)

        return articles

    def show(self, console):

        articles = self.get_articles()

        if len(articles) == 0:
            console.print("[yellow]История пока пуста[/yellow]")
            return

        console.print()

        console.print("[bold cyan]История статей[/bold cyan]")

        console.print("-" * 60)

        for i, article in enumerate(articles, start=1):

            console.print(
                f"{i}. {article['title']}\n"
                f"   ID: {article['id']}\n"
                f"   Дата: {article['created']}\n"
            )