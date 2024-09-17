import sqlite3
import os


# Функция для получения абсолютного пути к базе данных
def get_db_path():
    db_path = os.path.join(os.path.dirname(__file__), '../database/users.db')
    return db_path


# Создание базы данных и таблицы users
def create_db():
    db_path = get_db_path()
    print(f"Путь к базе данных: {db_path}")  # Для отладки
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создание таблицы
    print("Создаём таблицу users, если она не существует...")
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (chat_id INTEGER PRIMARY KEY, username TEXT, requested_cities TEXT)''')

    conn.commit()
    conn.close()
    print("Таблица users создана или уже существует.")
def register_user(chat_id, username):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (chat_id, username, requested_cities) VALUES (?, ?, ?)", (chat_id, username, ''))
    conn.commit()
    conn.close()

# Получение пользователя по chat_id
def get_user(chat_id):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE chat_id = ?", (chat_id,))
    return cursor.fetchone()