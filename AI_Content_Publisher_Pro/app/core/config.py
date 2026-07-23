import json

from dataclasses import dataclass

from dotenv import load_dotenv

from pathlib import Path

import os

from app.core.constants import CONFIG_FILE, ENV_FILE


load_dotenv(ENV_FILE)


@dataclass
class Settings:

    provider: str

    model: str

    language: str

    temperature: float

    max_tokens: int

    project: str

    output: dict

    seo: dict

    gemini_key: str


def load_settings():

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:

        cfg = json.load(f)

    return Settings(

        provider=cfg["provider"],

        model=cfg["model"],

        language=cfg["language"],

        temperature=cfg["temperature"],

        max_tokens=cfg["max_tokens"],

        project=cfg["project"],

        output=cfg["output"],

        seo=cfg["seo"],

        gemini_key=os.getenv("GEMINI_API_KEY", "")

    )


settings = load_settings()