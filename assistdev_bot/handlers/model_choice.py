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
        "🧠 <b>Какая нейросеть будет работать в вашем боте?</b>\n\n"
        "Вы можете не вникать в технические детали. Я объясню простыми словами:\n\n"
        "✅ <b>DeepSeek (рекомендую)</b> — современная, быстрая, стоит копейки "
        "(около 1 рубля за 1 000 сообщений). Подходит для большинства бизнесов.\n\n"
        "🆓 <b>OpenRouter (бесплатный)</b> — тоже работает, но может немного тормознуть "
        "при наплыве клиентов. Хорош для тестов или если у вас 10–20 вопросов в день.\n\n"
        "По качеству ответов они почти одинаковые. Я советую DeepSeek — он надёжнее. "
        "Цена копеечная, вы её не заметите. А Максим всё настроит.\n\n"
        "Какой вариант выберем?",
        reply_markup=model_choice_keyboard(),
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(OrderState.choosing_model, F.data.startswith("model_"))
async def model_chosen(callback: CallbackQuery, state: FSMContext):
    model = callback.data.split("_")[1]
    model_name = "DeepSeek" if model == "deepseek" else "OpenRouter"
    await state.update_data(ai_model=model, ai_model_name=model_name)
    await state.set_state(OrderState.choosing_extra)

    text = (
        "🛠 <b>Дополнительный пакет «Полная настройка под ключ»</b>\n\n"
        "Что включает:\n"
        "• Регистрация API-ключей (DeepSeek/OpenRouter) — сделаю за вас\n"
        "• Выбор и настройка хостинга (рекомендуется Railway)\n"
        "• Деплой бота и проверка работы\n"
        "• Обучение работе с ботом (1 час)\n\n"
        f"💰 Стоимость: <b>+1 500 ₽</b> (к стоимости услуги)\n"
        f"⏱ Доп. срок: +1 день\n\n"
        "Вам нужна эта услуга?"
    )
    await callback.message.edit_text(text, reply_markup=extra_package_choice(), parse_mode="HTML")
    await callback.answer()
