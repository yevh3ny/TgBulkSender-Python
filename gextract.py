from telethon.sync import TelegramClient
from config import APP_API_ID, APP_API_HASH, PHONE_NUMBER
# Введите данные для подключения к аккаунту Telegram
api_id = APP_API_ID
api_hash = APP_API_HASH
phone_number = PHONE_NUMBER

# Введите имя группы
group_username = input("Введите имя группы: ")

# Создайте TelegramClient и авторизуйтесь в аккаунте Telegram
with TelegramClient(phone_number, api_id, api_hash) as client:
    # Авторизуйтесь в аккаунте Telegram
    client.connect()

    if not client.is_user_authorized():
        client.send_code_request(phone_number)
        client.sign_in(phone_number, input(
            'Введите код подтверждения: '))

    try:
        # Получите информацию о группе
        group = client.get_entity(group_username)

        # Получите список участников группы
        participants = client.get_participants(group)

        # Выведите имена пользователей на экран
        for participant in participants:
            if participant.username:
                print(participant.username)
    except Exception as e:
        print(
            f"Ошибка при получении списка участников группы: {str(e)}")
