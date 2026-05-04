from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards.inline import back_button, final_actions
from services.ai_client import AIClient
from .menu import OrderState

router = Router()


@router.callback_query(F.data == "ask_question")
async def start_ai_consultant(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    service_name = data.get("service_name", "выбранной услуги")
    await state.update_data(consultant_service=service_name)
    await state.set_state(OrderState.asking_ai)
    await callback.answer()
    await callback.message.edit_text(
        f"💬 *Вы задаёте вопрос по услуге: {service_name}*\n\n"
        "Напишите, что вас интересует (сроки, технологии, возможности).\n"
        "Я отвечу конкретно по этой услуге.",
        reply_markup=back_button(),
        parse_mode="Markdown",
    )


@router.message(OrderState.asking_ai)
async def handle_ai_question(message: Message, state: FSMContext):
    data = await state.get_data()
    service_name = data.get("consultant_service", "выбранной услуге")

    prompt = (
        f'Ты — AI-консультант по услуге "{service_name}". '
        f"Пользователь задаёт вопрос именно по этой услуге. Не уточняй, какая услуга его интересует — ты уже знаешь. "
        f"Отвечай чётко, конкретно, используй эмодзи. "
        f"Общие сроки: от 2 часов до 2 дней. Цены фиксированные. Доп. пакет +1500₽."
    )

    ai_client = AIClient()
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": message.text},
    ]
    response = await ai_client.chat(messages, max_tokens=400)

    if not response:
        response = "❌ Извините, AI временно недоступен. Вернитесь к заказу или напишите Максиму."

    await state.set_state(OrderState.final_confirm)
    await message.delete()
    await message.answer(
        f"🤖 *Ответ:*\n\n{response}\n\n➡️ Продолжить оформление:",
        reply_markup=final_actions(),
        parse_mode="Markdown",
    )
