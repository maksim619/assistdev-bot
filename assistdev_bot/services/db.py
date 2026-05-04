import aiosqlite
from config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        with open("database/schema.sql", "r") as f:
            await db.executescript(f.read())
        await db.commit()

async def save_user(user_id, username, full_name):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, full_name) VALUES (?, ?, ?)",
            (user_id, username, full_name)
        )
        await db.commit()

async def save_order(user_id, service_name, service_price, extra_package, extra_price, total_price, client_name, contact, details):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO orders (user_id, service_name, service_price, extra_package, extra_price, total_price, client_name, contact, details) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (user_id, service_name, service_price, extra_package, extra_price, total_price, client_name, contact, details)
        )
        await db.commit()
        return cursor.lastrowid