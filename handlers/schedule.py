# handlers/schedule.py
from pyrogram import filters
from datetime import datetime, timedelta
import asyncio
from database import init_db

conn = init_db()
cursor = conn.cursor()

def add_schedule_handler(app):
    
    @app.on_message(filters.command("schedule"))
    async def schedule_message(client, message):
        try:
            parts = message.text.split(maxsplit=2)
            if len(parts) < 3:
                await message.reply("Usage: /schedule [minutes] [message]")
                return

            minutes = int(parts[1])
            scheduled_message = parts[2]

            if minutes <= 0:
                await message.reply("The number of minutes must be greater than zero.")
                return

            scheduled_time = datetime.now() + timedelta(minutes=minutes)

            # Insert the scheduled message into the database
            chat_id = message.chat.id
            user_id = message.from_user.id
            cursor.execute("INSERT INTO scheduled_messages (chat_id, user_id, message, scheduled_time) VALUES (?, ?, ?, ?)", 
                           (chat_id, user_id, scheduled_message, scheduled_time))
            conn.commit()

            await message.reply(f"Message scheduled to be sent in {minutes} minutes.")

        except ValueError:
            await message.reply("Invalid format. Usage: /schedule [minutes] [message]")


