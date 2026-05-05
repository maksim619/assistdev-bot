from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.inline import continue_or_back, main_menu, model_choice_keyboard, extra_package_choice
from services.instructions import SERVICE_DESCRIPTIONS

router = Router()


class OrderState(StatesGroup):
    selecting_service = State()
    service_detail = State()
    choosing_model = State()
    choosing_extra = State()
    filling_data = State()
    final_confirm = State()
    asking_ai = State()


@router.callback_query(F.data.startswith("service_"))
async def show_service_detail(callback: CallbackQuery, state: FSMContext):
    service_id = int(callback.data.split("_")[1])
    service = SERVICE_DESCRIPTIONS[service_id]
    await state.update_data(
        service_id=service_id,
        service_name=service["name"],
        service_price=service["price"],
    )
    await state.set_state(OrderState.service_detail)

    text = (
        f"📌 <b>{service['name']}</b>\n\n"
        f"💰 Цена: <b>{service['price']} ₽</b>\n\n"
        f"📋 <b>Что входит:</b>\n{service['desc']}\n\n"
        f"➡️ Нажмите «Продолжить», чтобы выбрать AI-модель для вашего бота."
    )
    await callback.answer()
    await callback.message.edit_text(text, reply_markup=continue_or_back(), parse_mode="HTML")


@router.callback_query(OrderState.service_detail, F.data == "back_to_services")
async def back_to_services(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await callback.message.edit_text(
        "🌟 <b>Главное меню</b>\n\nВыберите услугу:",
        reply_markup=main_menu(),
        parse_mode="HTML",
    )


@router.callback_query(OrderState.choosing_extra, F.data == "back_to_model_choice")
async def back_to_model_choice(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.choosing_model)
    await callback.message.edit_text(
        "🧠 <b>Выберите AI-модель для вашего будущего бота:</b>\n\n"
        "🔓 <b>OpenRouter (бесплатно)</b>\n"
        "— Модели: Llama 3, Mistral\n"
        "— Подходит для тестов и малой нагрузки\n\n"
        "💎 <b>DeepSeek (платный, ~0.14$/1М токенов)</b>\n"
        "— Профессиональное решение\n"
        "— Стабильность и скорость\n\n"
        "Какой вариант вам ближе?",
        reply_markup=model_choice_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(OrderState.choosing_model, F.data == "back_to_service_detail")
async def back_to_service_detail(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.service_detail)
    data = await state.get_data()
    service_id = data.get("service_id")
    if service_id:
        service = SERVICE_DESCRIPTIONS[service_id]
        text = (
            f"📌 <b>{service['name']}</b>\n\n"
            f"💰 Цена: <b>{service['price']} ₽</b>\n\n"
            f"📋 <b>Что входит:</b>\n{service['desc']}\n\n"
            f"➡️ Нажмите «Продолжить», чтобы выбрать AI-модель для вашего бота."
        )
        await callback.message.edit_text(text, reply_markup=continue_or_back(), parse_mode="HTML")
    await callback.answer()


@router.callback_query(OrderState.final_confirm, F.data == "back_to_extra")
async def back_to_extra(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.choosing_extra)
    text = (
        "🛠 <b>Дополнительный пакет «Полная настройка под ключ»</b>\n\n"
        "Что включает:\n"
        "• Регистрация API-ключей (DeepSeek/OpenRouter)\n"
        "• Выбор и настройка хостинга\n"
        "• Деплой бота и проверка\n"
        "• Обучение 1 час\n\n"
        "💰 Стоимость: +1 500 ₽\n"
        "Вам нужна эта услуга?"
    )
    await callback.message.edit_text(text, reply_markup=extra_package_choice(), parse_mode="HTML")
    await callback.answer()
