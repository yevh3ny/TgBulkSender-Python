import telebot
import sqlite3
from telebot import types

# Создаем экземпляр бота
bot = telebot.TeleBot('YOUR_BOT_TOKEN')

# Подключаемся к базе данных SQLite3
conn = sqlite3.connect('user_data.db')
cursor = conn.cursor()

# Создаем таблицу для хранения списка пользователей
cursor.execute('''CREATE TABLE IF NOT EXISTS send_list
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT)''')

# Создаем таблицу для хранения текста сообщения
cursor.execute('''CREATE TABLE IF NOT EXISTS send_text
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT)''')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    # Проверяем, является ли отправитель администратором
    if message.from_user.username == 'vorobyovevge':
        # Создаем клавиатуру главного меню
        markup = types.ReplyKeyboardMarkup(row_width=2)
        item1 = types.KeyboardButton('Введите список')
        item2 = types.KeyboardButton('Введите текст')
        markup.add(item1, item2)
        # Отправляем приветственное сообщение с главным меню
        bot.send_message(message.chat.id, 'Привет! Выберите действие:', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Извините, у вас нет доступа к этой команде.')

# Обработчик для команды "Введите список"
@bot.message_handler(func=lambda message: message.text == 'Введите список')
def enter_user_list(message):
    bot.send_message(message.chat.id, 'Введите список пользователей в формате:\nusername1\nusername2\nusername3')
    # Устанавливаем состояние ожидания списка пользователей
    bot.register_next_step_handler(message, save_user_list)

# Функция сохранения списка пользователей в базу данных
def save_user_list(message):
    user_list = message.text.split('\n')
    # Сохраняем список пользователей в базу данных
    for username in user_list:
        cursor.execute("INSERT INTO send_list (username) VALUES (?)", (username,))
        conn.commit()
    bot.send_message(message.chat.id, 'Список пользователей сохранен.')
    show_main_menu(message)

# Обработчик для команды "Введите текст"
@bot.message_handler(func=lambda message: message.text == 'Введите текст')
def enter_text(message):
    bot.send_message(message.chat.id, 'Введите текст сообщения:')
    # Устанавливаем состояние ожидания текста сообщения
    bot.register_next_step_handler(message, save_message_text)

# Функция сохранения текста сообщения в базу данных
def save_message_text(message):
    message_text = message.text
    # Сохраняем текст сообщения в базу данных
    cursor.execute("INSERT INTO send_text (message) VALUES (?)", (message_text,))
    conn.commit()
    bot.send_message(message.chat.id, 'Текст сообщения сохранен.')
    show_send_menu(message)

# Показать главное меню
def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('Введите список')
    item2 = types.KeyboardButton('Введите текст')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=markup)

# Показать меню отправки
def show_send_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton('Назад')
    item2 = types.KeyboardButton('Отправить')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Сообщение готово. Выберите действие:', reply_markup=markup)

# Обработчик для кнопки "Назад"
@bot.message_handler(func=lambda message: message.text == 'Назад')
def go_back(message):
    show_main_menu(message)

# Обработчик для кнопки "Отправить"
@bot.message_handler(func=lambda message: message.text == 'Отправить')
def send_message(message):
    # Получаем список пользователей из базы данных
    cursor.execute("SELECT username FROM send_list")
    user_list = cursor.fetchall()
    # Получаем текст сообщения из базы данных
    cursor.execute("SELECT message FROM send_text ORDER BY id DESC LIMIT 1")
    message_text = cursor.fetchone()

    # Отправляем сообщение каждому пользователю из списка
    for user in user_list:
        bot.send_message('@' + user[0], message_text[0])

    # Очищаем таблицу send_list
    cursor.execute("DELETE FROM send_list")
    conn.commit()

    # Очищаем таблицу send_text
    cursor.execute("DELETE FROM send_text")
    conn.commit()

    # Возвращаемся в главное меню
    show_main_menu(message)
print("Бот запущен")
# Запускаем бота
bot.polling()

# Закрываем соединение с базой данных
cursor.close()
conn.close()
