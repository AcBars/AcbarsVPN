import sqlite3
import os
import logging
import VPNKeyGenerator

DB_PATH = "users.db"

# Проверка наличия базы данных и её создание
if not os.path.exists(DB_PATH):
    open(DB_PATH, 'w').close()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY,
                  user_id INTEGER UNIQUE,
                  username TEXT,
                  full_name TEXT,
                  user_file TEXT)''')
conn.commit()


def get_user(user_id):
    cursor.execute("SELECT user_file FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None


def add_user(user_id, username, full_name, bot):
    user_file_content = f"User ID: {user_id}\nUsername: {username}\nFull Name: {full_name}\n"
    try:
        cursor.execute("INSERT INTO users (user_id, username, full_name, user_file) VALUES (?, ?, ?, ?)",
                       (user_id, username, full_name, user_file_content))
        conn.commit()
    except sqlite3.IntegrityError:
        logging.warning(f"Пользователь {user_id} уже существует в базе данных.")
        return get_user(user_id)

    if username and username != "Не указан":
        if VPNKeyGenerator.generate_client_keys(username):
            bot.send_message(user_id, f"Ключи OpenVPN для {username} успешно созданы.")
            return user_file_content
    return None
