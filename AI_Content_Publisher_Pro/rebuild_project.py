from pathlib import Path
import shutil

ROOT = Path(__file__).parent

old_root = ROOT / "app" / "app"
new_root = ROOT / "app"

folders = [
    "core",
    "history",
    "generators",
    "ui",
    "exporters",
]

for folder in folders:
    src = old_root / folder
    dst = new_root / folder

    if not src.exists():
        continue

    dst.mkdir(parents=True, exist_ok=True)

    for file in src.iterdir():
        target = dst / file.name

        if target.exists():
            print(f"Пропущен: {target.name}")
            continue

        shutil.move(str(file), str(target))
        print(f"Перенесен: {file.name}")

print("\nГотово.")

try:
    shutil.rmtree(old_root)
    print("Удалена папка app/app")
except Exception as e:
    print(e)