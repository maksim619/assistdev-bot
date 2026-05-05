from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from keyboards.inline import back_button, final_actions, main_menu, extra_package_choice
from services.instructions import EXTRA_PACKAGES, SERVICE_DESCRIPTIONS
from services.db import save_order, save_user
from config import DEV_ID
from .menu import OrderState
from bot_instance import bot
import html

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
        "📝 <b>Пожалуйста, введите ваши данные для связи:</b>\n\n"
        "Напишите одним сообщением:\n"
        "1. Ваше имя\n"
        "2. Контакт (Telegram username, телефон или email)\n\n"
        "Пример: <b>Иван, @ivan_123</b>",
        reply_markup=back_button(),
        parse_mode="HTML",
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
    service_id = user_data.get("service_id", 1)
    service_info = SERVICE_DESCRIPTIONS.get(service_id, SERVICE_DESCRIPTIONS[1])
    service_name = service_info["name"]
    service_price = user_data.get("service_price", service_info["price"])
    extra_package = user_data.get("extra_package", "none")
    extra_price = user_data.get("extra_price", 0)
    total = service_price + extra_price
    extra_desc = EXTRA_PACKAGES[extra_package]["name"] if extra_package != "none" else "Без доп. услуг"
    ai_model_name = user_data.get("ai_model_name", "DeepSeek")

    await state.update_data(
        total_price=total,
        service_name=service_name,
        service_price=service_price,
    )
    await state.set_state(OrderState.final_confirm)

    text = (
        f"📋 <b>Ваша заявка</b>\n\n"
        f"📌 Услуга: {html.escape(service_name)}\n"
        f"💰 Цена: <b>{service_price} ₽</b>\n"
        f"🧠 Модель AI: {html.escape(ai_model_name)}\n"
        f"🛠 Доп. пакет: {html.escape(extra_desc)} {'+' + str(extra_price) + '₽' if extra_price else ''}\n"
        f"💵 <b>Итого: {total} ₽</b>\n"
        f"👤 Имя: {html.escape(name)}\n"
        f"📞 Контакт: {html.escape(contact)}\n\n"
        f"⏱ <b>Общий срок: от 2 часов до 3 дней.</b>\n\n"
        f"Что делаем дальше?"
    )
    await message.delete()
    await message.answer(text, reply_markup=final_actions(), parse_mode="HTML")


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

    user_link = f"tg://user?id={user.id}"
    username = f"@{user.username}" if user.username else "нет username"
    dev_message = (
        f"🔔 <b>НОВЫЙ ЗАКАЗ!</b> (AssistDev)\n\n"
        f"👤 Клиент: {html.escape(data['client_name'])}\n"
        f"📞 Контакт: {html.escape(data['contact'])}\n"
        f"🔗 Telegram: {html.escape(username)} | <a href=\"{user_link}\">клик</a>\n"
        f"📋 Услуга: {html.escape(data['service_name'])} — {data['service_price']}₽\n"
        f"🧠 Модель AI: {html.escape(data.get('ai_model_name', 'DeepSeek'))}\n"
        f"🛠 Доп. пакет: {html.escape(data['extra_package'])} (+{data['extra_price']}₽)\n"
        f"💰 Итого: {data['total_price']}₽\n"
        f"📅 Заказ №{order_id}"
    )
    await bot.send_message(
        DEV_ID,
        dev_message,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

    await callback.message.edit_text(
        "✅ <b>Заказ отправлен!</b>\n\n"
        "Максим получил вашу заявку и свяжется с вами в ближайшее время.\n\n"
        "Спасибо! 🙌",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )
    await state.clear()
    await callback.answer()


@router.callback_query(OrderState.final_confirm, F.data == "back_to_extra")
async def back_to_extra(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.choosing_extra)
    text = (
        "🛠 <b>Дополнительный пакет «Полная настройка под ключ»</b>\n\n"
        "Что включает:\n"
        "• Регистрация API-ключей\n"
        "• Выбор и настройка хостинга\n"
        "• Деплой бота и проверка\n"
        "• Обучение 1 час\n\n"
        "💰 Стоимость: +1 500 ₽\n"
        "Вам нужна эта услуга?"
    )
    await callback.message.edit_text(text, reply_markup=extra_package_choice(), parse_mode="HTML")
    await callback.answer()
