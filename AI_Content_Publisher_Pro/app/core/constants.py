from pathlib import Path

APP_NAME = "AI Marketing Studio PRO"
APP_VERSION = "1.0.0"

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

CONFIG_FILE = ROOT_DIR / "config.json"

ENV_FILE = ROOT_DIR / ".env"

LOG_DIR = ROOT_DIR / "logs"

OUTPUT_DIR = ROOT_DIR / "outputs"

ARTICLE_DIR = ROOT_DIR / "articles"

DATABASE_DIR = ROOT_DIR / "database"

DATABASE_FILE = DATABASE_DIR / "database.db"