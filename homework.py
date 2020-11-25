import time
import requests
import os

from twilio.rest import Client


def get_status(user_id):
    params = {
        "user_ids": user_id,
        "v": 5.92,
        "fields": "online",
        "access_token": os.environ["ACCOUNT_TOKEN"],
    }
    url = "https://api.vk.com/method/users.get"
    user_info = requests.post(url, params=params)
    return user_info.json()["response"][0]["online"]  # Верните статус пользователя в ВК


def sms_sender(sms_text):
    account_sid = os.environ["ACCOUNT_SID"]
    auth_token = os.environ["TWILIO_ACCOUNT_TOKEN"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=sms_text,
        from_=os.environ["NUMBER_FROM"],
        to=os.environ["NUMBER_TO"],
    )
    return message.sid  # Верните sid отправленного сообщения из Twilio


if __name__ == '__main__':
    # тут происходит инициализация Client
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
