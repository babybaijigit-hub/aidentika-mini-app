"""Environment-based configuration. Secrets are never stored in source code."""
from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str
    webapp_url: str | None
    database_path: str


def load_settings() -> Settings:
    token = os.getenv("BOT_TOKEN", "").strip()
    if not token or token == "replace_with_your_telegram_bot_token":
        raise RuntimeError(
            "BOT_TOKEN is missing. Copy .env.example to .env and set the token locally."
        )
    webapp_url = os.getenv("WEBAPP_URL", "").strip() or None
    return Settings(
        bot_token=token,
        webapp_url=webapp_url,
        database_path=os.getenv("DATABASE_PATH", "data/study_assistant.sqlite3"),
    )
