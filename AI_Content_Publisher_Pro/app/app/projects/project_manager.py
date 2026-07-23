from pathlib import Path
import json

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)


class ProjectManager:

    def create(self, name):
        project = PROJECTS_DIR / name
        project.mkdir(exist_ok=True)

        (project / "outputs").mkdir(exist_ok=True)
        (project / "images").mkdir(exist_ok=True)
        (project / "prompts").mkdir(exist_ok=True)

        config = {
            "name": name,
            "language": "ru",
            "wordpress": {},
            "telegram": {}
        }

        with open(project / "config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

        return project

    def list(self):
        return [p.name for p in PROJECTS_DIR.iterdir() if p.is_dir()]