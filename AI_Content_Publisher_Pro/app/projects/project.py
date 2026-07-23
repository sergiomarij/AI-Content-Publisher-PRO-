from pathlib import Path
import json

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)


class Project:

    def __init__(self, name):

        self.name = name
        self.folder = PROJECTS_DIR / name

    def create(self):

        self.folder.mkdir(exist_ok=True)

        (self.folder / "templates").mkdir(exist_ok=True)

        cfg = {
            "name": self.name,
            "wordpress": {
                "url": "",
                "username": "",
                "application_password": ""
            },
            "telegram": {
                "token": "",
                "chat_id": ""
            },
            "dtf": {},
            "vc": {},
            "medium": {},
            "teletype": {}
        }

        with open(self.folder / "config.json", "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)

    def load(self):

        with open(self.folder / "config.json", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):

        with open(self.folder / "config.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
