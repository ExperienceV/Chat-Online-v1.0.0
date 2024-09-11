import sqlite3
import logging
from database.data_queries import user_data

# Conectar a la base de datos (la creará si no existe)
conn = sqlite3.connect('chat_realtime.db', isolation_level=None)
cursor = conn.cursor()

# Función para agregar un usuario
async def user_create(user_name, user_password) -> dict | bool:
    """ Crear un nuevo usuario verificando si el user_name ya existe """
    try:
        with conn:
            cursor.execute("INSERT INTO users(user_name, user_password) VALUES(?, ?)", (user_name, user_password))
            conn.commit()
        logging.info(f"Usuario '{user_name}' creado con éxito.")

        response: list | bool = await user_data(user_name)
        return response
    
    except sqlite3.IntegrityError:
        logging.error(f"Error: El usuario '{user_name}' ya existe.")
        return False
    except Exception as e:
        logging.error(e)
        return False




