import requests



def notify(BOT_TOKEN, CHAT_IDS, text):
    print("Notify: ", BOT_TOKEN, CHAT_IDS, text)
    url = f"https://api.telegram.org/bot{ BOT_TOKEN }/sendMessage"
    
    for chat_id in CHAT_IDS:
        requests.post(url, json={
            "chat_id": chat_id,
            "text": text
        })