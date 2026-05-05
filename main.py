import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'assistdev_bot'))

from config import BOT_TOKEN, DEEPSEEK_API_KEY, DEV_ID

required_vars = {
    "BOT_TOKEN": BOT_TOKEN,
    "DEV_ID": DEV_ID,
}
missing = [name for name, val in required_vars.items() if val is None or val == ""]
if missing:
    print(f"ОШИБКА: Не заданы переменные окружения: {', '.join(missing)}")
    print("Укажите их в панели Railway → Variables")
    sys.exit(1)

from bot import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
