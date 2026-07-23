from rich.console import Console

console = Console()


def menu(current):

    console.print()

    console.print("=" * 60)
    console.print("[bold cyan]PROJECT MANAGER[/bold cyan]")
    console.print("=" * 60)

    console.print(f"Текущий проект: [green]{current if current else 'не выбран'}[/green]")

    console.print()

    console.print("1. Выбрать проект")
    console.print("2. Создать проект")
    console.print("3. Переименовать проект")
    console.print("4. Удалить проект")
    console.print("5. Открыть папку проекта")

    console.print()

    console.print("0. Назад")
    console.print("=" * 60)