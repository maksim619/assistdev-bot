from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards.inline import back_button, final_actions, main_menu, extra_package_choice
from services.instructions import EXTRA_PACKAGES
from services.db import save_order, save_user
from config import DEV_ID
from .menu import OrderState
from bot_instance import bot

router = Router()


@router.callback_query(OrderState.choosing_extra, F.data.startswith("extra_"))
async def select_extra(callback: CallbackQuery, state: FSMContext):
    extra_type = callback.data.split("_")[1]
    package = "full_setup" if extra_type == "full" else "none"
    await state.update_data(
        extra_package=package,
        extra_price=EXTRA_PACKAGES[package]["price"],
    )
    await state.set_state(OrderState.filling_data)
    await callback.answer()
    await callback.message.edit_text(
        "📝 *Пожалуйста, введите ваши данные для связи:*\n\n"
        "Напишите одним сообщением:\n"
        "1. Ваше имя\n"
        "2. Контакт (Telegram username, телефон или email)\n\n"
        "Пример: *Иван, @ivan_123*",
        reply_markup=back_button(),
        parse_mode="Markdown",
    )


@router.message(OrderState.filling_data)
async def receive_client_data(message: Message, state: FSMContext):
    data = message.text.strip()
    if len(data) < 5:
        await message.answer("❌ Введите имя и контакт (минимум 5 символов).")
        return

    parts = data.split(",")
    name = parts[0].strip()
    contact = parts[1].strip() if len(parts) > 1 else parts[0].strip()
    await state.update_data(client_name=name, contact=contact)

    user_data = await state.get_data()
    service_name = user_data["service_name"]
    service_price = user_data["service_price"]
    extra_package = user_data["extra_package"]
    extra_price = user_data["extra_price"]
    total = service_price + extra_price
    extra_desc = EXTRA_PACKAGES[extra_package]["name"] if extra_package != "none" else "Без доп. услуг"
    ai_model_name = user_data.get("ai_model_name", "DeepSeek")

    await state.update_data(total_price=total)
    await state.set_state(OrderState.final_confirm)

    text = (
        f"📋 *Ваша заявка*\n\n"
        f"📌 Услуга: {service_name}\n"
        f"💰 Цена: {service_price} ₽\n"
        f"🧠 Модель AI: {ai_model_name}\n"
        f"🛠 Доп. пакет: {extra_desc} {'+' + str(extra_price) + '₽' if extra_price else ''}\n"
        f"💵 *Итого: {total} ₽*\n"
        f"👤 Имя: {name}\n"
        f"📞 Контакт: {contact}\n\n"
        f"⏱ Общий срок: от 2 часов до 2 дней.\n\n"
        f"Что делаем дальше?"
    )
    await message.delete()
    await message.answer(text, reply_markup=final_actions(), parse_mode="Markdown")


@router.callback_query(OrderState.final_confirm, F.data == "final_order")
async def place_order(callback: CallbackQuery, state: FSMContext):
    user = callback.from_user
    await save_user(user.id, user.username, user.full_name)

    data = await state.get_data()
    order_id = await save_order(
        user_id=user.id,
        service_name=data["service_name"],
        service_price=data["service_price"],
        extra_package=data["extra_package"],
        extra_price=data["extra_price"],
        total_price=data["total_price"],
        client_name=data["client_name"],
        contact=data["contact"],
        details=f"Модель AI: {data.get('ai_model_name')}, Доп. пакет: {data['extra_package']}",
    )

    dev_message = (
        f"🔔 НОВЫЙ ЗАКАЗ! (AssistDev)\n\n"
        f"👤 Клиент: @{user.username or user.first_name} (ID: {user.id})\n"
        f"📋 Услуга: {data['service_name']} — {data['service_price']}₽\n"
        f"🧠 Модель AI: {data.get('ai_model_name')}\n"
        f"🛠 Доп. пакет: {data['extra_package']} (+{data['extra_price']}₽)\n"
        f"💰 Итого: {data['total_price']}₽\n"
        f"👤 Имя: {data['client_name']}\n"
        f"📞 Контакт: {data['contact']}\n"
        f"📅 Заказ №{order_id}"
    )
    await bot.send_message(DEV_ID, dev_message)

    await callback.message.edit_text(
        "✅ *Заказ отправлен!*\n\n"
        "Максим получил вашу заявку и свяжется с вами в ближайшее время.\n\n"
        "Спасибо! 🙌",
        reply_markup=main_menu(),
        parse_mode="Markdown",
    )
    await state.clear()
    await callback.answer()
