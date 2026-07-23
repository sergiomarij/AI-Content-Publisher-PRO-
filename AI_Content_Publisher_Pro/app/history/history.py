from pathlib import Path
import json


class HistoryManager:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir

    def get_articles(self) -> list[dict]:
        """Return generated articles from the selected project's output folder."""
        result = []

        if not self.output_dir.exists():
            return result

        for folder in self.output_dir.iterdir():
            if not folder.is_dir():
                continue

            meta = folder / "meta.json"
            if meta.exists():
                try:
                    with meta.open(encoding="utf-8") as file:
                        result.append(json.load(file))
                except (OSError, json.JSONDecodeError):
                    continue

        result.sort(key=lambda article: article.get("created", ""), reverse=True)

        return result
