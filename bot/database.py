"""Small SQLite persistence layer for user requests."""
import json
from datetime import datetime, timezone
from pathlib import Path

import aiosqlite


class Database:
    def __init__(self, path: str) -> None:
        self.path = path

    async def initialize(self) -> None:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                """CREATE TABLE IF NOT EXISTS requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_user_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    result_text TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )"""
            )
            await db.commit()

    async def save_request(
        self, user_id: int, category: str, payload: dict, result: str
    ) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                "INSERT INTO requests (telegram_user_id, category, payload_json, result_text, created_at) VALUES (?, ?, ?, ?, ?)",
                (
                    user_id,
                    category,
                    json.dumps(payload, ensure_ascii=False),
                    result,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            await db.commit()
