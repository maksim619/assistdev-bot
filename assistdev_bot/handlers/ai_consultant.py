from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from keyboards.inline import back_button, final_actions, main_menu
from services.ai_client import AIClient
from .menu import OrderState
from bot_instance import bot
import html

router = Router()


@router.callback_query(F.data == "ask_question")
async def start_ai_consultant(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    service_name = data.get("service_name", "выбранной услуги")
    await state.update_data(consultant_service=service_name)
    await state.set_state(OrderState.asking_ai)
    await callback.answer()
    await callback.message.edit_text(
        f"💬 <b>Вы задаёте вопрос по услуге:</b> {html.escape(service_name)}\n\n"
        "Напишите, что вас интересует (сроки, технологии, возможности).\n"
        "Я отвечу конкретно по этой услуге.",
        reply_markup=back_button(),
        parse_mode="HTML",
    )


@router.message(OrderState.asking_ai)
async def handle_ai_question(message: Message, state: FSMContext):
    # Показываем «печатает...»
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")

    data = await state.get_data()
    service_name = data.get("consultant_service", "выбранной услуге")
    prompt = (
        f'Ты — AI-консультант по услуге "{service_name}". '
        f"Пользователь уже выбрал эту услугу. Отвечай только по ней, не уточняй, какая его интересует. "
        f"Будь дружелюбным, используй эмодзи, давай чёткие ответы. "
        f"Сроки выполнения: от 2 часов до 3 дней (в зависимости от сложности и текущей загрузки). "
        f"Цены фиксированные (указаны в описании услуги). Доп. пакет полной настройки +1500₽. "
        f"Не придумывай скидки. Будь вежливым."
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
        f"🤖 <b>Ответ:</b>\n\n{html.escape(response)}\n\n➡️ Продолжить оформление:",
        reply_markup=final_actions(),
        parse_mode="HTML",
    )
