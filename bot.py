# bot.py
from pyrogram import Client
from config import api_id, api_hash, bot_token
from handlers import add_handlers, add_imposter_handlers
from handlers.schedule import add_schedule_handler
from schedule_check import check_scheduled_messages
import asyncio

# Initialize bot
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Register command handlers
add_handlers(app)
add_imposter_handlers(app)
add_schedule_handler(app)

async def main():
    await app.start()
    await check_scheduled_messages(app)

if __name__ == "__main__":
    app.start()
    asyncio.get_event_loop().run_until_complete(check_scheduled_messages(app))
    app.idle()
