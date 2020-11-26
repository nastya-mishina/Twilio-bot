import time
import requests
import os
from twilio.rest import Client
import logging

access_token = os.environ["VK_TOKEN"]
version_api = 5.92

def get_status(user_id):
    base_url = "https://api.vk.com/method/{}"
    method = "users.get"
    params = {
        "user_ids": user_id,
        "version_api": version_api,
        "fields": "online",
        "access_token": access_token,
    }
    url = base_url.format(method)
    try:
        user_info = requests.post(url, params=params)
    except Exception as ex:
        logging.error("Error at %s", "request post", exc_info=ex)
    return user_info.json().get("response")[0].get("online")

def sms_sender(sms_text):
    account_sid = os.environ["ACCOUNT_SID"]
    auth_token = os.environ["AUTH_TOKEN"]
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms_text,
        from_=os.environ["NUMBER_FROM"],
        to=os.environ["NUMBER_TO"],
    )
    return message.sid

if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f"{vk_id} сейчас онлайн!")
            break
        time.sleep(5)
