import requests

TELEGRAM_TOKEN = "7300638793:AAHQh0fw_vX2K1uoeoaNtA2iHIjGNg68HR8"
CHAT_ID = "271366313"

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
