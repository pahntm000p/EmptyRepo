# handlers/imposter.py
from pyrogram import filters
from database import init_db

conn = init_db()
cursor = conn.cursor()

# Define the non-command filter
non_command_filter = filters.group & ~filters.regex(r"^/")

def add_imposter_handlers(app):

    @app.on_message(filters.command("imposter"))
    async def imposter_mode(client, message):
        chat_id = message.chat.id
        if len(message.command) == 2:
            option = message.command[1].lower()
            if option == "on":
                cursor.execute("INSERT OR REPLACE INTO imposter_mode (chat_id, is_enabled) VALUES (?, ?)", (chat_id, True))
                conn.commit()
                await message.reply("Imposter mode has been enabled in this chat.")
            elif option == "off":
                cursor.execute("INSERT OR REPLACE INTO imposter_mode (chat_id, is_enabled) VALUES (?, ?)", (chat_id, False))
                conn.commit()
                await message.reply("Imposter mode has been disabled in this chat.")
            else:
                await message.reply("Usage: /imposter on | off")
        else:
            await message.reply("Usage: /imposter on | off")

    @app.on_message(non_command_filter)
    async def detect_name_change(client, message):
        chat_id = message.chat.id
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name

        cursor.execute("SELECT is_enabled FROM imposter_mode WHERE chat_id = ?", (chat_id,))
        row = cursor.fetchone()
        if row and row[0]:
            cursor.execute("SELECT username, first_name, last_name FROM users WHERE user_id = ?", (user_id,))
            user_row = cursor.fetchone()
            if user_row:
                old_username, old_first_name, old_last_name = user_row
                if username != old_username or first_name != old_first_name or last_name != old_last_name:
                    changes = []
                    if username != old_username:
                        changes.append(f"🔄 **Username:** {old_username} ➜ {username}")
                    if first_name != old_first_name or last_name != old_last_name:
                        changes.append(f"🔄 **Name:** {old_first_name} {old_last_name} ➜ {first_name} {last_name}")
                    
                    changes_message = "\n".join(changes)
                    await message.reply(
                        f"🚨 **User ID {user_id}** has made changes!\n\n{changes_message}\n\n🔍 Please take note of the update!"
                    )
                    cursor.execute("UPDATE users SET username = ?, first_name = ?, last_name = ? WHERE user_id = ?", 
                                   (username, first_name, last_name, user_id))
                    cursor.execute("INSERT INTO name_history (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)", 
                                   (user_id, username, first_name, last_name))
                    conn.commit()
            else:
                cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)", 
                               (user_id, username, first_name, last_name))
                cursor.execute("INSERT INTO name_history (user_id, username, first_name, last_name) VALUES (?, ?, ?, ?)", 
                               (user_id, username, first_name, last_name))
                conn.commit()

    @app.on_message(filters.command("all"))
    async def get_name_history(client, message):
        if len(message.command) == 2:
            user_id = int(message.command[1])
            cursor.execute("SELECT username, first_name, last_name, change_date FROM name_history WHERE user_id = ? ORDER BY change_date", 
                           (user_id,))
            rows = cursor.fetchall()
            if rows:
                history = "\n\n".join(
                    [f"📅 **Date:** {row[3]}\n**Username:** {row[0]}\n**Name:** {row[1]} {row[2]}" for row in rows]
                )
                # Split the history message into parts if it exceeds the Telegram message limit
                max_length = 4096  # Telegram message character limit
                parts = [history[i:i+max_length] for i in range(0, len(history), max_length)]
                
                for part in parts:
                    await message.reply(part)
            else:
                await message.reply("No history found for this user.")
        else:
            await message.reply("Usage: /all {user_id}")
