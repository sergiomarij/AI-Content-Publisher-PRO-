from rich.console import Console
from rich.panel import Panel

console=Console()

def main():
    console.print(Panel.fit("AI Content Publisher PRO (Recovery Mode)"))
    while True:
        console.print("\n1. SEO статья\n2. WordPress\n3. Проекты\n4. История\n0. Выход")
        c=input("Выберите пункт: ").strip()
        if c=="0":
            break
        console.print("[yellow]Модуль временно отключён до восстановления main.py[/yellow]")

if __name__=="__main__":
    main()
