from rich.console import Console

console = Console()


def show_menu():

    console.print()

    console.print("=" * 60)
    console.print("[bold cyan]AI Content Publisher PRO[/bold cyan]")
    console.print("=" * 60)

    items = [
        "SEO статья",
        "WordPress",
        "Telegram",
        "DTF",
        "VC.ru",
        "Medium",
        "Teletype",
        "История",
        "Экспорт",
        "Проекты",
        "Настройки"
    ]

    for i, item in enumerate(items, start=1):
        console.print(f"{i}. {item}")

    console.print("0. Выход")
    console.print("=" * 60)