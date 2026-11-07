"""FSM handlers for the implemented first bot milestone."""
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot.keyboards import MENU_ITEMS, main_menu
from bot.services.outlines import make_presentation_outline, make_work_outline

router = Router()
WORK_TYPES = [
    "Реферат", "Курсовая работа", "СРС", "Дипломная работа", "Эссе", "Доклад",
    "Научная статья", "Практическая работа", "Лабораторная работа", "Бизнес-план",
    "Исследовательский проект", "Отчёт по практике", "Сочинение", "Изложение",
    "Анализ литературного произведения", "Мотивационное письмо", "Резюме (CV)",
]
LANGUAGES = ["Русский", "Кыргызский", "English"]


class WorkForm(StatesGroup):
    kind = State()
    topic = State()
    subject = State()
    volume = State()
    language = State()
    requirements = State()
    sources = State()


class PresentationForm(StatesGroup):
    topic = State()
    slides = State()
    language = State()
    style = State()


def options_keyboard(options: list[str]) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=value)] for value in options]
        + [[KeyboardButton(text="↩️ Главное меню"), KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


@router.message(F.text == "📚 Учебные работы")
async def start_work(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(WorkForm.kind)
    await message.answer("Выберите вид учебной работы:", reply_markup=options_keyboard(WORK_TYPES))


@router.message(WorkForm.kind)
async def work_kind(message: Message, state: FSMContext) -> None:
    if message.text not in WORK_TYPES:
        await message.answer("Выберите вид работы кнопкой из списка или нажмите «Отмена».")
        return
    await state.update_data(kind=message.text)
    await state.set_state(WorkForm.topic)
    await message.answer("Напишите тему работы:", reply_markup=ReplyKeyboardRemove())


@router.message(WorkForm.topic)
async def work_topic(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not value:
        await message.answer("Тема не должна быть пустой. Напишите тему текстом:")
        return
    await state.update_data(topic=value[:300])
    await state.set_state(WorkForm.subject)
    await message.answer("Укажите предмет:")


@router.message(WorkForm.subject)
async def work_subject(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not value:
        await message.answer("Предмет не должен быть пустым. Укажите предмет:")
        return
    await state.update_data(subject=value[:150])
    await state.set_state(WorkForm.volume)
    await message.answer("Укажите объём (например, 8 страниц):")


@router.message(WorkForm.volume)
async def work_volume(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not value:
        await message.answer("Укажите объём, например: 8 страниц.")
        return
    await state.update_data(volume=value[:80])
    await state.set_state(WorkForm.language)
    await message.answer("На каком языке подготовить план?", reply_markup=options_keyboard(LANGUAGES))


@router.message(WorkForm.language)
async def work_language(message: Message, state: FSMContext) -> None:
    if message.text not in LANGUAGES:
        await message.answer("Выберите язык кнопкой из списка.")
        return
    await state.update_data(language=message.text)
    await state.set_state(WorkForm.requirements)
    await message.answer("Требования преподавателя? Напишите их или отправьте «нет»:", reply_markup=ReplyKeyboardRemove())


@router.message(WorkForm.requirements)
async def work_requirements(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    await state.update_data(requirements="" if text.lower() in {"нет", "no", "жок"} else text[:1500])
    await state.set_state(WorkForm.sources)
    await message.answer("Добавить раздел для источников?", reply_markup=options_keyboard(["Да", "Нет"]))


@router.message(WorkForm.sources)
async def work_sources(message: Message, state: FSMContext, db, webapp_url: str | None = None) -> None:
    if message.text not in {"Да", "Нет"}:
        await message.answer("Выберите «Да» или «Нет» кнопкой.")
        return
    await state.update_data(sources=message.text)
    data = await state.get_data()
    result = make_work_outline(data)
    await db.save_request(message.from_user.id, "study_work", data, result)
    await state.clear()
    await message.answer(result[:4000], reply_markup=main_menu(webapp_url))


@router.message(F.text == "📊 Презентации")
async def start_presentation(message: Message, state: FSMContext) -> None:
    await state.clear()
    await state.set_state(PresentationForm.topic)
    await message.answer("Напишите тему презентации:", reply_markup=ReplyKeyboardRemove())


@router.message(PresentationForm.topic)
async def presentation_topic(message: Message, state: FSMContext) -> None:
    value = (message.text or "").strip()
    if not value:
        await message.answer("Тема не должна быть пустой. Напишите тему презентации:")
        return
    await state.update_data(topic=value[:300])
    await state.set_state(PresentationForm.slides)
    await message.answer("Сколько слайдов нужно? Укажите число от 3 до 20:")


@router.message(PresentationForm.slides)
async def presentation_slides(message: Message, state: FSMContext) -> None:
    try:
        slides = int((message.text or "").strip())
    except ValueError:
        await message.answer("Введите целое число от 3 до 20.")
        return
    if not 3 <= slides <= 20:
        await message.answer("Количество слайдов должно быть от 3 до 20.")
        return
    await state.update_data(slides=str(slides))
    await state.set_state(PresentationForm.language)
    await message.answer("Выберите язык:", reply_markup=options_keyboard(LANGUAGES))


@router.message(PresentationForm.language)
async def presentation_language(message: Message, state: FSMContext) -> None:
    if message.text not in LANGUAGES:
        await message.answer("Выберите язык кнопкой из списка.")
        return
    await state.update_data(language=message.text)
    await state.set_state(PresentationForm.style)
    await message.answer("Какой стиль оформления предпочитаете?", reply_markup=options_keyboard(["Минималистичный", "Академический", "Яркий"]))


@router.message(PresentationForm.style)
async def presentation_style(message: Message, state: FSMContext, db, webapp_url: str | None = None) -> None:
    if message.text not in {"Минималистичный", "Академический", "Яркий"}:
        await message.answer("Выберите стиль кнопкой из списка.")
        return
    await state.update_data(style=message.text)
    data = await state.get_data()
    result = make_presentation_outline(data)
    await db.save_request(message.from_user.id, "presentation", data, result)
    await state.clear()
    await message.answer(result[:4000], reply_markup=main_menu(webapp_url))


@router.message(F.text.in_(MENU_ITEMS))
async def planned_modules(message: Message) -> None:
    await message.answer(
        "Этот раздел пока не реализован. На первом этапе доступны учебный план работы и структура презентации."
    )
