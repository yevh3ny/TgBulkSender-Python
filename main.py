import sqlite3
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser
from config import APP_API_ID, APP_API_HASH, PHONE_NUMBER

# Введите данные для подключения к аккаунту Telegram
api_id = APP_API_ID
api_hash = APP_API_HASH
phone_number = PHONE_NUMBER

# Введите путь к базе данных SQLite
db_path = 'user_data.db'

# Установите соединение с базой данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создайте таблицу send_list, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS send_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT)''')

# Создайте таблицу send_text, если она не существует
cursor.execute('''CREATE TABLE IF NOT EXISTS send_text (message TEXT)''')

# Запросите список имен пользователей
usernames_input = input(
    "Введите список имен пользователей, разделенных переносом строки:\n")

# Разделите введенный список на отдельные имена пользователей
usernames = usernames_input.strip().split('\n')

# Запросите текст сообщения
message_text = input("Введите текст сообщения:\n")

# Сохраните список пользователей в базе данных
for username in usernames:
    cursor.execute("INSERT INTO send_list (username) VALUES (?)", (username,))
    conn.commit()

# Сохраните текст сообщения в базе данных
cursor.execute("INSERT INTO send_text (message) VALUES (?)", (message_text,))
conn.commit()

# Подключитесь к аккаунту Telegram
with TelegramClient('session', api_id, api_hash) as client:
    # Авторизуйтесь в аккаунте Telegram
    client.connect()

    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input(
            'Введите код подтверждения: '))

    # Отправьте сообщение каждому пользователю из списка
    for username in usernames:
        try:
            # Получите ID пользователя на основе его имени
            user = client.get_input_entity(username)

            # Отправьте сообщение от вашего аккаунта Telegram пользователю
            client.send_message(user, message_text)
            print(
                f"Сообщение отправлено пользователю {username}")
        except Exception as e:
            print(
                f"Ошибка при отправке сообщения пользователю {username}: {str(e)}")

# Выведите сообщение о завершении процесса
print("Рассылка сообщений завершена")

conn.close()
