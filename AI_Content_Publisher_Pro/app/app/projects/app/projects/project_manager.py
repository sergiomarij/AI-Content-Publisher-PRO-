from pathlib import Path
import json

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)


class ProjectManager:

    def create(self, name: str):

        project = PROJECTS_DIR / name

        if project.exists():
            return False

        project.mkdir()

        (project / "outputs").mkdir()
        (project / "images").mkdir()
        (project / "prompts").mkdir()

        config = {
            "name": name,
            "language": "ru",
            "wordpress": {
                "url": "",
                "login": "",
                "password": ""
            },
            "telegram": {
                "token": "",
                "chat_id": ""
            }
        }

        with open(project / "config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        return True

    def projects(self):

        return sorted(
            [x.name for x in PROJECTS_DIR.iterdir() if x.is_dir()]
        )