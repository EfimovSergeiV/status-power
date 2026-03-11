import os, requests

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN", "TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "123456")

def notify(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })