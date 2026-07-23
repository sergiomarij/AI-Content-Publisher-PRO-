import json
from pathlib import Path

from app.projects.current import CurrentProject


class WordPressConfig:

    def __init__(self):

        self.current = CurrentProject()

    def _config_file(self):

        project = self.current.get()

        if not project:
            raise Exception("Не выбран активный проект.")

        return Path("projects") / project / "config.json"

    def load(self):

        file = self._config_file()

        with open(file, encoding="utf-8") as f:
            cfg = json.load(f)

        return cfg["wordpress"]

    def save(self, url, username, password):

        file = self._config_file()

        with open(file, encoding="utf-8") as f:
            cfg = json.load(f)

        cfg["wordpress"] = {
            "url": url,
            "username": username,
            "application_password": password
        }

        with open(file, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)