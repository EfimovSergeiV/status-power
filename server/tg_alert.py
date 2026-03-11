import requests


def notify(BOT_TOKEN, CHAT_ID, text):
    print("Notify: ", BOT_TOKEN, CHAT_ID, text)
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })