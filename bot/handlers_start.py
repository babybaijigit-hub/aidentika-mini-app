"""Start command, menu navigation, cancellation, and profile placeholder."""
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.keyboards import main_menu

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext, webapp_url: str | None = None) -> None:
    await state.clear()
    await message.answer(
        "Привет! Я AI Study Assistant. Сейчас доступны шаблон учебной работы и структура презентации. "
        "AI-генерация, экспорт и остальные разделы будут добавляться отдельно.",
        reply_markup=main_menu(webapp_url),
    )


@router.message(F.text.in_({"↩️ Главное меню", "🏠 Главное меню"}))
async def go_home(message: Message, state: FSMContext, webapp_url: str | None = None) -> None:
    await state.clear()
    await message.answer("Главное меню:", reply_markup=main_menu(webapp_url))


@router.message(F.text == "❌ Отмена")
async def cancel(message: Message, state: FSMContext, webapp_url: str | None = None) -> None:
    await state.clear()
    await message.answer("Действие отменено.", reply_markup=main_menu(webapp_url))
