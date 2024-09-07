import sqlite3
from datetime import datetime
import logging
from database.data_queries import user_data

# Conectar a la base de datos (la creará si no existe)
conn = sqlite3.connect('chat_realtime.db', isolation_level=None)
cursor = conn.cursor()


# Crear la tabla users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL UNIQUE,
    user_password TEXT NOT NULL
)
''')

# Crear la tabla messages
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
)
''')

# Función para agregar un usuario
async def user_create(user_name, user_password) -> dict | bool:
    """ Crear un nuevo usuario verificando si el user_name ya existe """
    try:
        with conn:
            cursor.execute("INSERT INTO users(user_name, user_password) VALUES(?, ?)", (user_name, user_password))
            conn.commit()
        logging.info(f"Usuario '{user_name}' creado con éxito.")

        response: list | bool = await user_data(user_name)

        if response:
            user_dict: dict = {
                "id" : response[0],
                "user_name" : response[1],
                "user_password" : response[2]
            }

        return user_dict
    except sqlite3.IntegrityError:
        logging.error(f"Error: El usuario '{user_name}' ya existe.")
        return False
    except Exception as e:
        logging.error(e)
        return False

async def user_login(user_name, user_password) -> dict | bool:
    """ Iniciar sesión si el usuario existe """
    try:
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND user_password = ?", (user_name, user_password))
        result = cursor.fetchone()
        print(result)
        if result:
            user_dict = {
                "id" : result[0],
                "user_name" : result[1],
                "user_password" : result[2]
            }
            return user_dict
        logging.error(f"Error: El usuario '{user_name}' no existe o la contraseña es incorrecta.")
        return False
    except Exception as e:
        logging.error(e)
        return False




# Función para agregar un mensaje
def add_message(user_id, text):
    try:
        with conn:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('INSERT INTO messages (user_id, text, timestamp) VALUES (?, ?, ?)',
                        (user_id, text, timestamp))
            conn.commit()
        return cursor.lastrowid
    except Exception as e:
        logging.error(e)
        return None



