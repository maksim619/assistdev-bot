# AssistDev Bot 🤖

AI-секретарь для продажи кастомных Telegram-ботов. Автоматически общается с клиентами, обсуждает детали, оформляет заказы и пересылает их разработчику.

## Функциональность

- **5 типов услуг** с фиксированными ценами:
  - FAQ-бот — 7 000 ₽
  - HR-бот-скринер — 8 000 ₽
  - Сентимент-анализ — 9 000 ₽
  - Бот записи — 11 000 ₽
  - RAG-ассистент — 15 000 ₽
- Доп. услуга "Полная настройка под ключ" — +1 500 ₽
- Интеллектуальный AI-секретарь на базе DeepSeek (с фолбэком на OpenRouter)
- Выбор модели ИИ для реализации (OpenRouter бесплатно / DeepSeek платно)
- Интеграция с SQLite для хранения заказов
- Админ-панель для управления заказами

## Технологии

- **Python 3.10+**
- **aiogram 3.x** — асинхронный фреймворк для Telegram
- **OpenAI SDK** — для DeepSeek и OpenRouter API
- **aiosqlite** — асинхронный SQLite
- **pydantic** — валидация данных
- **FSM** — машина состояний диалога

## Структура проекта

```
assistdev_bot/
├── bot.py                  # Точка входа
├── config.py               # Конфигурация (.env)
├── handlers/
│   ├── commands.py         # /start, /admin, /help
│   ├── menu.py             # Кнопки и выбор услуг
│   ├── ai_dialog.py        # AI-общение
│   └── order.py            # Обработка заказов
├── services/
│   ├── ai_client.py        # Клиент DeepSeek/OpenRouter
│   ├── db.py               # Операции с БД
│   └── instructions.py     # Статические тексты
├── keyboards/
│   └── inline.py           # Инлайн-клавиатуры
├── models/
│   └── schemas.py          # Pydantic-модели
├── database/
│   └── schema.sql          # Схема БД
├── .env.example            # Шаблон конфига
└── requirements.txt        # Зависимости
```

## Быстрый старт

### 1. Установка зависимостей

**Windows:**
```bat
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

Или вручную:
```bash
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate.bat на Windows
pip install -r requirements.txt
```

### 2. Настройка конфигурации

Скопируйте `.env.example` в `.env` и заполните:

```env
BOT_TOKEN=ваш_токен_бота_от_BotFather
DEEPSEEK_API_KEY=sk-ваш_ключ_DeepSeek
OPENROUTER_API_KEY=sk-ваш_ключ_OpenRouter
DEV_ID=ваш_telegram_user_id (число)
DB_PATH=assistdev.db
```

Как получить:
- **BOT_TOKEN** — @BotFather → /newbot
- **DEEPSEEK_API_KEY** — platform.deepseek.com → API Keys
- **OPENROUTER_API_KEY** — openrouter.ai → Keys
- **DEV_ID** — @userinfobot

### 3. Запуск бота

```bash
# Активируйте окружение (если не активно)
source venv/bin/activate  # или venv\Scripts\activate.bat

# Запускаем
python -m assistdev_bot.bot
```

Бот запустится и отправит уведомление разработчику.

## Использование

### Клиентская сторона

1. **/start** — начать диалог, выбрать услугу
2. Выбрать услугу из списка
3. Обсудить детали с AI-секретарём (можно спрашивать про хостинг, регистрацию, модели)
4. Выбрать модель ИИ (OpenRouter / DeepSeek)
5. Доп. настройка (+1 500 ₽)
6. Подтвердить заказ и оставить контакт

### Разработчик (админ)

- **/admin** — панель управления заказами
- В панели можно менять статусы: new → in_work → completed

### Ручные заявки

Кнопка "✍️ Оставить заявку вручную" позволяет клиенту написать свободный текст, который сразу перешлётся разработчику.

## Системный промпт AI

AI-секретарь использует следующий системный промпт (на русском):

```
Ты — AI-секретарь бота AssistDev. Твоя задача — помочь клиенту выбрать одну из пяти услуг...
```

Полный текст находится в `services/instructions.py`.

## База данных

### Таблицы

- **users** — пользователи (user_id, username, full_name, created_at)
- **dialog_states** — текущие состояния диалога (FSM контекст)
- **orders** — история заказов

Инициализация выполняется автоматически при запуске (`database/schema.sql`).

## Обработка ошибок

- При ошибке DeepSeek AI автоматически фолбэчит на OpenRouter
- При неудаче обоих провайдеров — пользователю предлагается ручная заявка
- Ошибки логируются в консоль

## Требования

- Python 3.10+
- Виртуальное окружение (venv)
- Аккаунт на DeepSeek и/или OpenRouter для API ключей
- Бот зарегистрирован в @BotFather

## Лицензия

Проект создан для коммерческого использования. Все права на код — разработчику.

## Поддержка

По вопросам: @username_разработчика (указать в .env)

---

**AssistDev** — ваш умный помощник в продаже ботов! 🚀
