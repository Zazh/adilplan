import requests
import os

TELEGRAM_TOKEN = os.getenv("SECRET_KEY_TG")
CHAT_ID =  os.getenv("SECRET_KEY_TG_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    try:
        requests.post(url, data=data, timeout=5)
    except Exception as e:
        # В логах увидишь ошибку, если что-то не так
        print("TELEGRAM ERROR", e)
