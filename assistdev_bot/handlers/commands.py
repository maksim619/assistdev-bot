from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline import main_menu, back_button

CHANNEL_LINK = "https://t.me/AssistDev619"
CHANNEL_USERNAME = "https://t.me/AssistDev619"

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🌟 *Привет! Я личный ассистент Максима.*\n\n"
        "Максим — разработчик ботов на AI. Помогу вам выбрать и заказать решение.\n\n"
        "📋 *Цены (фикс, сроки от 2 часов до 2 дней):*\n"
        "• FAQ-бот — 7 000₽\n"
        "• HR-бот — 8 000₽\n"
        "• Анализ отзывов — 9 000₽\n"
        "• Запись к специалисту — 11 000₽\n"
        "• RAG-ассистент — 15 000₽\n\n"
        "➕ *Доп. пакет:* полная настройка под ключ +1 500₽\n\n"
        "👇 Выберите услугу:",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "❓ *Помощь*\n\n"
        "1. Выберите услугу из меню.\n"
        "2. Нажмите «Продолжить» → выберите AI-модель.\n"
        "3. Выберите доп. пакет (или откажитесь).\n"
        "4. Введите имя и контакт.\n"
        "5. Нажмите «Заказать» — Максим получит заявку.\n\n"
        "Если вопрос по услуге — нажмите «Задать вопрос».",
        reply_markup=back_button(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🌟 Главное меню\n\nВыберите услугу:",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )


@router.callback_query(F.data == "reviews")
async def reviews_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        f'<b>📢 Оставить отзыв о работе Максима</b>\n\n'
        f'Присоединяйтесь к нашему каналу: {CHANNEL_LINK}\n\n'
        f'Там вы можете:\n'
        f'✅ Прочитать мнения других клиентов\n'
        f'📝 Написать свой отзыв (я опубликую его)\n\n'
        f'Спасибо, что помогаете становиться лучше! 🙌',
        parse_mode="HTML",
        reply_markup=back_button(),
    )


@router.callback_query(F.data == "help")
async def help_callback(callback: CallbackQuery):
    await callback.answer()
    await cmd_help(callback.message)
