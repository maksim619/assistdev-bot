from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    buttons = [
        [InlineKeyboardButton(text="🤖 FAQ-бот (5 000₽)", callback_data="service_1")],
        [InlineKeyboardButton(text="📄 HR-бот (6 000₽)", callback_data="service_2")],
        [InlineKeyboardButton(text="💬 Анализ отзывов (7 000₽)", callback_data="service_3")],
        [InlineKeyboardButton(text="📅 Запись к специалисту (9 000₽)", callback_data="service_4")],
        [InlineKeyboardButton(text="📚 RAG-ассистент (15 000₽)", callback_data="service_5")],
        [InlineKeyboardButton(text="🍽️ Ресторан/кафе (12 000₽)", callback_data="service_6")],
        [InlineKeyboardButton(text="☕ Кофейня (8 000₽)", callback_data="service_7")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_menu")],
    ])


def continue_or_back():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Продолжить", callback_data="continue_extra")],
        [InlineKeyboardButton(text="🔙 Назад к услугам", callback_data="back_to_services")],
    ])


def model_choice_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔓 OpenRouter (бесплатно)", callback_data="model_openrouter")],
        [InlineKeyboardButton(text="💎 DeepSeek (платный)", callback_data="model_deepseek")],
        [InlineKeyboardButton(text="🔙 Назад к услуге", callback_data="back_to_service_detail")],
    ])


def extra_package_choice():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, полная настройка (+1 500₽)", callback_data="extra_full")],
        [InlineKeyboardButton(text="❌ Нет, только бот (0₽)", callback_data="extra_none")],
        [InlineKeyboardButton(text="🔙 Назад к выбору модели", callback_data="back_to_model_choice")],
    ])


def final_actions():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Заказать услугу", callback_data="final_order")],
        [InlineKeyboardButton(text="❓ Задать вопрос по услуге", callback_data="ask_question")],
        [InlineKeyboardButton(text="🔙 Назад к доп. пакету", callback_data="back_to_extra")],
    ])
