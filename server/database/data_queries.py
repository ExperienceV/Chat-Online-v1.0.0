import sqlite3
import logging


conn = sqlite3.connect('chat_realtime.db', isolation_level=None)
cursor = conn.cursor()

async def user_data(user_name):
    try:
        with conn:
            result = cursor.execute("SELECT * FROM users WHERE user_name = ?", (user_name,))
            return result.fetchone()
    except Exception as e:
        logging.error(e)
        return None
    



    