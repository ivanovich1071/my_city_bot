import sqlite3
import os

# Функция для получения абсолютного пути к базе данных
def get_db_path():
    # Абсолютный путь к файлу базы данных
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'database/users.db'))
    print(f"Путь к базе данных: {db_path}")  # Для отладки
    return db_path

# Функция для чтения данных из таблицы users
def read_users():
    db_path = get_db_path()

    # Проверяем, существует ли файл базы данных
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Файл базы данных не найден: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Выполняем запрос на чтение данных
    cursor.execute("SELECT * FROM users")

    # Получаем все строки
    rows = cursor.fetchall()

    # Закрываем соединение с базой данных
    conn.close()

    # Возвращаем полученные строки
    return rows

# Чтение данных из БД и вывод их на экран
try:
    users = read_users()

    # Если данные есть, выводим их
    if users:
        print("Список пользователей в базе данных:")
        for user in users:
            print(f"ID: {user[0]}, Имя: {user[1]}, Города: {user[2]}")
    else:
        print("В базе данных нет пользователей.")
except FileNotFoundError as e:
    print(e)
except sqlite3.OperationalError as e:
    print(f"Ошибка доступа к базе данных: {e}")
