# scheduled_sender.py
import asyncio
from datetime import datetime
from pyrogram import Client
from database import init_db

conn = init_db()
cursor = conn.cursor()

async def check_scheduled_messages(app):
    while True:
        now = datetime.now()
        cursor.execute("SELECT id, chat_id, message FROM scheduled_messages WHERE scheduled_time <= ?", (now,))
        messages_to_send = cursor.fetchall()

        for message in messages_to_send:
            message_id, chat_id, text = message
            await app.send_message(chat_id, text)
            cursor.execute("DELETE FROM scheduled_messages WHERE id = ?", (message_id,))
            conn.commit()

        # Sleep for a while before checking again
        await asyncio.sleep(1)  # Check every minute
