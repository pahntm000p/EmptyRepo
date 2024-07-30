# handlers/commands.py
from pyrogram import filters
from database import init_db

# Initialize the database
conn = init_db()
cursor = conn.cursor()

def add_handlers(app):

    @app.on_message(filters.command("start"))
    async def start(client, message):
        user_id = message.from_user.id
        username = message.from_user.username
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
        await message.reply("Hello! I'm your bot. Your information has been saved.")

    @app.on_message(filters.command("help"))
    async def help(client, message):
        await message.reply("Available commands: /start, /help")
