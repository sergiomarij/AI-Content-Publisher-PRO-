from pathlib import Path

from app.projects.project import Project

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)


class ProjectManager:

    def list(self):

        return sorted(
            [
                p.name
                for p in PROJECTS_DIR.iterdir()
                if p.is_dir()
            ]
        )

    def create(self, name):

        if (PROJECTS_DIR / name).exists():
            return False

        Project(name).create()

        return True

    def delete(self, name):

        import shutil

        folder = PROJECTS_DIR / name

        if folder.exists():
            shutil.rmtree(folder)

    def rename(self, old, new):

        (PROJECTS_DIR / old).rename(PROJECTS_DIR / new)
