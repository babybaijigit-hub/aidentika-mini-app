"""Run the Telegram bot with long polling."""
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import load_settings
from bot.database import Database
from bot.handlers import router as workflow_router
from bot.handlers_start import router as start_router


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = load_settings()
    db = Database(settings.database_path)
    await db.initialize()

    bot = Bot(token=settings.bot_token)
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.workflow_data.update(db=db, webapp_url=settings.webapp_url)
    dispatcher.include_router(start_router)
    dispatcher.include_router(workflow_router)
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
