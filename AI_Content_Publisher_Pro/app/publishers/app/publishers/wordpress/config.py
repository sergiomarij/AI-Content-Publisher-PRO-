import json
from pathlib import Path

CONFIG_FILE = Path("config.json")


class WordPressConfig:

    def load(self):

        if not CONFIG_FILE.exists():

            return {
                "url": "",
                "username": "",
                "application_password": ""
            }

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        return cfg.get("wordpress", {})

    def save(self, url, username, password):

        if CONFIG_FILE.exists():

            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)

        else:

            cfg = {}

        cfg["wordpress"] = {
            "url": url,
            "username": username,
            "application_password": password
        }

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)