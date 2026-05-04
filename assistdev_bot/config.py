import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEV_ID = int(os.getenv("DEV_ID", 0))
DB_PATH = os.getenv("DB_PATH", "assistdev.db")