import json
import os
import subprocess
from pathlib import Path

from rich.console import Console

from app.ui import banner, show_menu
from app.ui.dashboard import Dashboard
from app.core.config import settings
from app.core.logger import logger
from app.core.session import Base, engine
from app.generators.seo import SEOGenerator
from app.generators.telegram import TelegramGenerator
from app.generators.news import NewsGenerator
from app.generators.review import ReviewGenerator
from app.core.article_manager import ArticleManager
from app.projects.manager import ProjectManager
from app.projects.current import CurrentProject
from app.projects.menu import menu as project_menu
from app.history.history_manager import HistoryManager
from app.publishers.wordpress.menu import menu as wp_menu
from app.publishers.wordpress.config import WordPressConfig
from app.publishers.wordpress.client import WordPressClient
from app.publishers.wordpress.publisher import WordPressPublisher

console = Console()
dashboard = Dashboard()
pm = ProjectManager()
current = CurrentProject()


def generate_and_save(generator, topic: str, articles: ArticleManager):
    console.print("\n[cyan]Генерируем контент...[/cyan]\n")
    content = generator.generate(topic)
    article_id, folder = articles.create_article(topic)
    articles.save_markdown(folder, content)
    articles.save_html(folder, content)
    articles.save_text(folder, content)
    console.print(f"\n[green]Контент сохранён[/green] ({article_id})")
    return article_id


def handle_wordpress(wp: WordPressConfig, publisher: WordPressPublisher):
    while True:
        wp_menu()
        cmd = input("> ").strip()

        if cmd == "0":
            break

        try:
            if cmd == "1":
                url = input("URL сайта: ").strip()
                login = input("Логин: ").strip()
                password = input("Application Password: ").strip()
                wp.save(url, login, password)
                console.print("[green]Настройки сохранены[/green]")

            elif cmd == "2":
                cfg = wp.load()
                client = WordPressClient(
                    cfg["url"],
                    cfg["username"],
                    cfg["application_password"],
                )
                if client.test():
                    console.print("[green]Соединение успешно[/green]")
                else:
                    console.print("[red]Ошибка подключения[/red]")

            elif cmd == "3":
                ok, msg = publisher.publish_last(status="draft")
                console.print(f"[green]{msg}[/green]" if ok else f"[red]{msg}[/red]")

            elif cmd == "4":
                ok, msg = publisher.publish_last(status="publish")
                console.print(f"[green]{msg}[/green]" if ok else f"[red]{msg}[/red]")

            elif cmd == "5":
                ok, result = publisher.list_categories()
                if ok:
                    for cat in result:
                        console.print(f"  {cat.get('id')}. {cat.get('name')}")
                else:
                    console.print(f"[red]{result}[/red]")

            elif cmd == "6":
                ok, result = publisher.list_tags()
                if ok:
                    for tag in result:
                        console.print(f"  {tag.get('id')}. {tag.get('name')}")
                else:
                    console.print(f"[red]{result}[/red]")

            elif cmd == "7":
                cfg = wp.load()
                client = WordPressClient(
                    cfg["url"],
                    cfg["username"],
                    cfg["application_password"],
                )
                filepath = input("Путь к файлу: ").strip()
                path = Path(filepath)
                if not path.is_file():
                    console.print("[red]Файл не найден[/red]")
                    continue
                data = path.read_bytes()
                response = client.upload_media(path.name, data)
                if response.status_code in (200, 201):
                    console.print(f"[green]Медиа загружено: {response.json().get('source_url')}[/green]")
                else:
                    console.print(f"[red]{response.text}[/red]")

        except Exception as e:
            console.print(f"[red]{e}[/red]")


def handle_projects():
    while True:
        project_menu(current.get())
        cmd = input("> ").strip()

        if cmd == "0":
            break

        if cmd == "1":
            projects = pm.list()
            if not projects:
                console.print("[yellow]Нет проектов[/yellow]")
                continue
            console.print()
            for i, p in enumerate(projects, 1):
                console.print(f"{i}. {p}")
            n = input("\nВыберите проект: ").strip()
            try:
                current.set(projects[int(n) - 1])
                console.print("[green]Проект выбран[/green]")
            except (ValueError, IndexError):
                console.print("[red]Ошибка выбора[/red]")

        elif cmd == "2":
            name = input("Название проекта: ").strip()
            if not name:
                continue
            if pm.create(name):
                current.set(name)
                console.print("[green]Проект создан[/green]")
            else:
                console.print("[red]Такой проект уже существует[/red]")

        elif cmd == "3":
            old = current.get()
            if not old:
                console.print("[yellow]Нет активного проекта[/yellow]")
                continue
            new = input("Новое название: ").strip()
            if new:
                pm.rename(old, new)
                current.set(new)
                console.print("[green]Проект переименован[/green]")

        elif cmd == "4":
            old = current.get()
            if not old:
                console.print("[yellow]Нет активного проекта[/yellow]")
                continue
            ans = input(f"Удалить '{old}'? (y/n): ").strip()
            if ans.lower() == "y":
                pm.delete(old)
                current_file = Path("projects/current.txt")
                if current_file.exists():
                    current_file.unlink()
                console.print("[green]Проект удалён[/green]")

        elif cmd == "5":
            proj = current.get()
            if not proj:
                console.print("[yellow]Нет активного проекта[/yellow]")
                continue
            folder = Path("projects") / proj
            if folder.is_dir():
                if os.name == "nt":
                    os.startfile(folder)
                else:
                    subprocess.run(["xdg-open", str(folder)], check=False)
                console.print(f"[green]Открыта папка: {folder}[/green]")


def handle_export(articles: HistoryManager):
    items = articles.get_articles()
    if not items:
        console.print("[yellow]Нет статей для экспорта[/yellow]")
        return

    console.print()
    for i, a in enumerate(items, 1):
        console.print(f"{i}. {a['title']} ({a['id']})")

    n = input("\nВыберите статью: ").strip()
    try:
        article = items[int(n) - 1]
    except (ValueError, IndexError):
        console.print("[red]Неверный номер[/red]")
        return

    folder = Path(article["folder"])
    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)

    for ext in ("md", "html", "txt"):
        src = folder / f"article.{ext}"
        if src.exists():
            dst = export_dir / f"{article['id']}.{ext}"
            dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
            console.print(f"[green]Экспортировано:[/green] {dst}")


def handle_settings():
    console.print()
    console.print("[bold cyan]Настройки[/bold cyan]")
    console.print(f"  Provider:   {settings.provider}")
    console.print(f"  Model:      {settings.model}")
    console.print(f"  Language:   {settings.language}")
    console.print(f"  Temperature:{settings.temperature}")
    console.print(f"  Max tokens: {settings.max_tokens}")
    console.print(f"  Project:    {settings.project}")
    console.print()
    console.print(f"  Config:     {Path('config.json').resolve()}")
    console.print(f"  Gemini key: {'[OK] zadan' if settings.gemini_key else '[!] ne zadan'}")
    console.print()


def handle_telegram(articles: ArticleManager):
    topic = input("\nВведите тему поста: ").strip()
    if not topic:
        return
    try:
        generate_and_save(TelegramGenerator(), topic, articles)
    except Exception as e:
        console.print(f"[red]{e}[/red]")


def handle_platform(name: str, generator, articles: ArticleManager):
    topic = input(f"\nВведите тему для {name}: ").strip()
    if not topic:
        return
    try:
        generate_and_save(generator, topic, articles)
    except Exception as e:
        console.print(f"[red]{e}[/red]")


def main():
    Base.metadata.create_all(engine)

    banner(console)
    dashboard.show(console)

    logger.info("Проект запущен")

    seo = SEOGenerator()
    articles = ArticleManager()
    history = HistoryManager()
    wp = WordPressConfig()
    publisher = WordPressPublisher()

    console.print(f"[green]Provider:[/green] {settings.provider}")
    console.print(f"[green]Model:[/green] {settings.model}")

    while True:
        show_menu()
        choice = input("Выберите пункт: ").strip()

        if choice == "0":
            break

        elif choice == "1":
            topic = input("\nВведите тему статьи: ").strip()
            if not topic:
                continue
            try:
                generate_and_save(seo, topic, articles)
            except Exception as e:
                console.print(f"[red]{e}[/red]")

        elif choice == "2":
            handle_wordpress(wp, publisher)

        elif choice == "3":
            handle_telegram(articles)

        elif choice == "4":
            handle_platform("DTF", NewsGenerator(), articles)

        elif choice == "5":
            handle_platform("VC.ru", NewsGenerator(), articles)

        elif choice == "6":
            handle_platform("Medium", ReviewGenerator(), articles)

        elif choice == "7":
            handle_platform("Teletype", ReviewGenerator(), articles)

        elif choice == "8":
            history.show(console)

        elif choice == "9":
            handle_export(history)

        elif choice == "10":
            handle_projects()

        elif choice == "11":
            handle_settings()

        else:
            console.print("[yellow]Неверный пункт меню[/yellow]")


if __name__ == "__main__":
    main()
