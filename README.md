# AI Study Assistant

## Текущая проверенная область
Этот репозиторий содержит статический Telegram Mini App на GitHub Pages и отдельный Python-бот на aiogram 3. На первом этапе бот формирует шаблонные планы учебных работ и презентаций, а Mini App формирует локальный план в браузере. Это ещё не AI-генерация и не экспорт файлов.

## Проверки
Из корня репозитория запустите:

```bash
python -m unittest discover -s tests
python -m compileall -q bot
```

Бот использует SQLite. Установка зависимостей:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r bot/requirements.txt
```

## Запуск Telegram-бота
1. Скопируйте `.env.example` в `.env`.
2. Вставьте токен BotFather в `BOT_TOKEN` **только в локальном `.env`**. Никогда не загружайте `.env` в GitHub и не отправляйте токен в чат.
3. Запустите из корня проекта:

```bash
python -m bot.main
```

Затем откройте бота в Telegram, нажмите Start и проверьте учебную работу, презентацию, «Отмена» и возврат в главное меню. Long polling требует, чтобы этот процесс оставался запущенным; не запускайте два экземпляра одновременно.

Если проверяется только сайт, он опубликован по адресу: https://babybaijigit-hub.github.io/aidentika-mini-app/. Отправка Mini App в Telegram будет подключена отдельным шагом.

## Следующие этапы
1. Проверить локальный бот и Mini App.
2. Подключить Mini App к боту.
3. Добавить AI через секреты хостинга, затем функции и экспорт отдельными этапами.
