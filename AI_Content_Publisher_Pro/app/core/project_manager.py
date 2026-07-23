from pathlib import Path
import json


PROJECTS_DIR = Path("projects")
ACTIVE_PROJECT_FILE = ".active_project.json"


class ProjectManager:
    """Creates and lists local content projects."""

    def __init__(self, projects_dir: Path = PROJECTS_DIR):
        self.projects_dir = projects_dir
        self.projects_dir.mkdir(exist_ok=True)

    def create(self, name: str) -> Path:
        clean_name = self._validate_name(name)
        project = self.projects_dir / clean_name

        if project.exists():
            raise FileExistsError(f"Проект «{clean_name}» уже существует.")

        project.mkdir()
        for folder_name in ("outputs", "images", "prompts"):
            (project / folder_name).mkdir()

        config = {
            "name": clean_name,
            "language": "ru",
            "wordpress": {},
            "telegram": {},
        }
        with (project / "config.json").open("w", encoding="utf-8") as file:
            json.dump(config, file, indent=4, ensure_ascii=False)

        return project

    def list(self) -> list[str]:
        return sorted(
            project.name
            for project in self.projects_dir.iterdir()
            if project.is_dir()
        )

    def activate(self, name: str) -> Path:
        clean_name = self._validate_name(name)
        project = self.projects_dir / clean_name

        if not project.is_dir():
            raise FileNotFoundError(f"Проект «{clean_name}» не найден.")

        with (self.projects_dir / ACTIVE_PROJECT_FILE).open("w", encoding="utf-8") as file:
            json.dump({"name": clean_name}, file, ensure_ascii=False)

        return project

    def get_active(self) -> str | None:
        active_file = self.projects_dir / ACTIVE_PROJECT_FILE
        if not active_file.is_file():
            return None

        try:
            with active_file.open("r", encoding="utf-8") as file:
                name = json.load(file).get("name")
        except (OSError, json.JSONDecodeError):
            return None

        if isinstance(name, str) and (self.projects_dir / name).is_dir():
            return name
        return None

    def get_active_output_dir(self) -> Path | None:
        active_project = self.get_active()
        if active_project is None:
            return None
        return self.projects_dir / active_project / "outputs"

    @staticmethod
    def _validate_name(name: str) -> str:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Название проекта не может быть пустым.")
        if any(character in '<>:"/\\|?*' for character in clean_name):
            raise ValueError("Название содержит недопустимые символы.")
        return clean_name
