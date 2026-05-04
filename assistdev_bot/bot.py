import asyncio
import logging
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot_instance import bot
from handlers import commands, menu, model_choice, order_flow, ai_consultant
from services.db import init_db

logging.basicConfig(level=logging.INFO)

dp = Dispatcher(storage=MemoryStorage())


async def main():
    await init_db()
    dp.include_router(commands.router)
    dp.include_router(menu.router)
    dp.include_router(model_choice.router)
    dp.include_router(order_flow.router)
    dp.include_router(ai_consultant.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
