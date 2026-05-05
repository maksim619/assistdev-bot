import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'assistdev_bot'))

from bot import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")
