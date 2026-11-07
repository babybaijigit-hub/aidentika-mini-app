"""Telegram keyboards."""
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

MENU_ITEMS = [
    "📚 Учебные работы", "📊 Презентации", "🧮 Решение задач",
    "📸 Задания по фото", "🌍 Перевод и языки", "🧠 AI-репетитор",
    "📝 Тесты и экзамены", "🔍 Поиск источников", "📅 Планировщик",
    "👤 Мой профиль", "⚙️ Настройки",
]


def main_menu(webapp_url: str | None = None) -> ReplyKeyboardMarkup:
    rows = [
        [KeyboardButton(text="📚 Учебные работы"), KeyboardButton(text="📊 Презентации")],
        [KeyboardButton(text="🧮 Решение задач"), KeyboardButton(text="📸 Задания по фото")],
        [KeyboardButton(text="🌍 Перевод и языки"), KeyboardButton(text="🧠 AI-репетитор")],
        [KeyboardButton(text="📝 Тесты и экзамены"), KeyboardButton(text="🔍 Поиск источников")],
        [KeyboardButton(text="📅 Планировщик"), KeyboardButton(text="👤 Мой профиль")],
        [KeyboardButton(text="⚙️ Настройки")],
    ]
    if webapp_url:
        rows.append([KeyboardButton(text="🌐 Открыть Mini App", web_app=WebAppInfo(url=webapp_url))])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True, input_field_placeholder="Выберите раздел")
