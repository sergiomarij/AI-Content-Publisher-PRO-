from pathlib import Path
from rich.panel import Panel
from rich.table import Table

from app.projects.current import CurrentProject


class Dashboard:

    def show(self, console):

        current = CurrentProject().get()

        table = Table(show_header=False)

        table.add_row("Проект", current if current else "не выбран")

        table.add_row("WordPress", self.status_wp(current))
        table.add_row("Telegram", "❌")
        table.add_row("DTF", "❌")
        table.add_row("VC.ru", "❌")
        table.add_row("Medium", "❌")
        table.add_row("Teletype", "❌")

        outputs = Path("outputs")

        count = len(list(outputs.glob("ART-*")))

        table.add_row("Статей", str(count))

        console.print(
            Panel(
                table,
                title="AI Content Publisher PRO",
                border_style="cyan"
            )
        )

    def status_wp(self, project):

        if not project:
            return "❌"

        cfg = Path("projects") / project / "config.json"

        if not cfg.exists():
            return "❌"

        import json

        with open(cfg, encoding="utf-8") as f:
            data = json.load(f)

        if data["wordpress"]["url"]:
            return "✅"

        return "❌"