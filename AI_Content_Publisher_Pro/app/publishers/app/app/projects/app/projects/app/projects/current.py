from pathlib import Path

CURRENT = Path("projects/current.txt")


class CurrentProject:

    def get(self):

        if not CURRENT.exists():
            return None

        return CURRENT.read_text(encoding="utf-8").strip()

    def set(self, name):

        CURRENT.write_text(name, encoding="utf-8")