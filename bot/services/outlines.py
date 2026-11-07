"""Template study outlines; AI generation will be added in a later stage."""


def make_work_outline(payload: dict[str, str]) -> str:
    title = payload["topic"]
    subject = payload["subject"]
    kind = payload["kind"]
    volume = payload["volume"]
    language = payload["language"]
    requirements = payload["requirements"] or "Не указаны"
    sources = payload["sources"]

    body = [
        f"Учебный план: {kind}",
        f"Тема: {title}",
        f"Предмет: {subject}",
        f"Объём: {volume}",
        f"Язык: {language}",
        "",
        "1. Введение",
        f"   Объясните актуальность темы «{title}», сформулируйте цель и 2–4 задачи.",
        "2. Основная часть",
        f"   Глава 1 — основные понятия и контекст темы по предмету «{subject}».",
        "   Глава 2 — разбор ключевых фактов, аргументов или примеров.",
        "   Глава 3 — результаты анализа (если соответствуют требованиям задания).",
        "3. Заключение",
        "   Кратко ответьте на поставленные задачи и сформулируйте выводы.",
    ]
    if sources == "Да":
        body.extend(["4. Источники", "   Добавьте только реально проверенные книги и материалы; проверьте автора, название и год."])
    body.extend(["", f"Требования преподавателя: {requirements}", "", "Это план-заготовка, а не сгенерированная работа. Проверьте факты и правила учебного заведения."])
    return "\n".join(body)


def make_presentation_outline(payload: dict[str, str]) -> str:
    count = max(3, min(int(payload["slides"]), 20))
    lines = [
        f"План презентации: {payload['topic']}",
        f"Язык: {payload['language']} | Стиль: {payload['style']}",
        "",
    ]
    for number in range(1, count + 1):
        if number == 1:
            heading = "Титульный слайд"
        elif number == count:
            heading = "Выводы"
        else:
            heading = f"Ключевой аспект {number - 1}: изучите тему «{payload['topic']}»"
        lines.extend([f"Слайд {number}. {heading}", "  Добавьте краткий тезис, подтверждённый факт и подходящее изображение."])
    lines.extend(["", "Это шаблон структуры слайдов; файл PPTX пока не создаётся."])
    return "\n".join(lines)
