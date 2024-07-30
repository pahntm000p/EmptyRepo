# database.py
import sqlite3

def init_db():
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    
    # Create the users table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT)''')
    
    # Create the imposter_mode table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS imposter_mode (
                        chat_id INTEGER PRIMARY KEY,
                        is_enabled BOOLEAN)''')

    # Create the name_history table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS name_history (
                        user_id INTEGER,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create the scheduled_messages table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS scheduled_messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        chat_id INTEGER,
                        user_id INTEGER,
                        message TEXT,
                        scheduled_time TIMESTAMP)''')


    conn.commit()
    return conn
