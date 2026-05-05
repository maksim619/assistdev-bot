from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.inline import main_menu

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🌟 <b>Привет! Я личный ассистент Максима.</b>\n\n"
        "Помогаю заказать умного бота под ваш бизнес.\n\n"
        "👇 Выберите услугу:",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🌟 <b>Главное меню</b>\n\nВыберите услугу:",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )
