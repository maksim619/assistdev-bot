from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.inline import model_choice_keyboard, extra_package_choice
from .menu import OrderState

router = Router()


@router.callback_query(F.data == "continue_extra")
async def ask_model_choice(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.choosing_model)
    await callback.message.edit_text(
        "🧠 *Выберите AI-модель для вашего будущего бота:*\n\n"
        "🔓 *OpenRouter (бесплатно)*\n"
        "— Модели: Llama 3, Mistral\n"
        "— Подходит для тестов и малой нагрузки (до 100 запросов/день)\n"
        "— Нет расходов на API\n\n"
        "💎 *DeepSeek (платный, ~0.14$/1М токенов)*\n"
        "— Профессиональное решение\n"
        "— Быстрый ответ, стабильность\n"
        "— Для продакшена и большого трафика\n\n"
        "Какой вариант вам ближе?",
        reply_markup=model_choice_keyboard(),
        parse_mode="Markdown",
    )
    await callback.answer()


@router.callback_query(OrderState.choosing_model, F.data.startswith("model_"))
async def model_chosen(callback: CallbackQuery, state: FSMContext):
    model = callback.data.split("_")[1]
    model_name = "DeepSeek (платный)" if model == "deepseek" else "OpenRouter (бесплатный)"
    await state.update_data(ai_model=model, ai_model_name=model_name)
    await state.set_state(OrderState.choosing_extra)

    text = (
        "🛠 *Дополнительный пакет «Полная настройка под ключ»*\n\n"
        "Что включает:\n"
        "• Регистрация API-ключей (DeepSeek/OpenRouter) — сделаю за вас\n"
        "• Выбор и настройка хостинга (рекомендуется Railway)\n"
        "• Деплой бота и проверка работы\n"
        "• Обучение работе с ботом (1 час)\n\n"
        f"💰 Стоимость: *+1 500 ₽* (к стоимости услуги)\n"
        f"⏱ Доп. срок: +1 день\n\n"
        "Вам нужна эта услуга?"
    )
    await callback.message.edit_text(text, reply_markup=extra_package_choice(), parse_mode="Markdown")
    await callback.answer()
