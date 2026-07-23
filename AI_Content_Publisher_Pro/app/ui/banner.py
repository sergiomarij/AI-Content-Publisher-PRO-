from rich.panel import Panel


def show(console):

    console.print(
        Panel.fit(
            "[bold cyan]AI Content Publisher PRO[/bold cyan]\n"
            "[green]Version 2.0[/green]",
            border_style="cyan"
        )
    )
