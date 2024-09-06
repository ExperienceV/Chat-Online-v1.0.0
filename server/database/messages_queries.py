import sqlite3
import logging


conn = sqlite3.connect('chat_realtime.db', isolation_level=None)
cursor = conn.cursor()

async def save_message(user_id: int, text: str):
    try:
        with conn:
            cursor.execute("INSERT INTO messages(user_id, text) VALUES(?, ?)", (user_id, text))
            return True
    except Exception as e:
        logging.error(e)
        return None
    

async def whole_messages():
    try:
        with conn:
            messages = cursor.execute("SELECT * FROM messages")
            return messages.fetchall()

    except Exception as e:
        logging.error(e)
        return None
    



    