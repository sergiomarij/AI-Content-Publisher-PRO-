from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


def save_markdown(title: str, text: str, output_dir: Path = OUTPUT_DIR):

    output_dir.mkdir(parents=True, exist_ok=True)

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    path = output_dir / f"{filename}.md"

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(text)

    return path
