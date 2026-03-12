import os, asyncio, secrets, requests
from fastapi import FastAPI, Request
from datetime import datetime

from tg_alert import notify

app = FastAPI()


def getenv(name, default=None, random_len=None):
    """ Возвращает переменную окружения """
    value = os.getenv(name)

    if value:
        return value
    if random_len:
        return secrets.token_hex(random_len)

    return default



TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN", random_len=16)
PING_TIMEOUT = int(getenv("PING_TIMEOUT", default="180"))


def get_chat_ids():
    response = requests.get(f"https://api.telegram.org/bot{ TELEGRAM_TOKEN }/getUpdates").json()
    messages = response.get("result")
    
    if messages:

        for msg in messages:
            chat = msg.get("message").get("chat")
            id, username = chat.get("id"), chat.get("username")

            if id not in chat_ids:
                chat_ids.append(id)


last_ping = None
power_off_notified = False
chat_ids = []

async def monitor():
    global last_ping, power_off_notified, chat_ids

    get_chat_ids()

    while True:
        await asyncio.sleep(60)

        if last_ping is None:
            continue

        diff = (datetime.utcnow() - last_ping).total_seconds()

        if diff > PING_TIMEOUT and not power_off_notified:
            print("Power OFF")
            notify(TELEGRAM_TOKEN, chat_ids, "⚠️ Power OFF detected!")
            power_off_notified = True

        if diff <= PING_TIMEOUT and power_off_notified:
            print("Power ON")
            notify(TELEGRAM_TOKEN, chat_ids, "✅ Power ON detected!")
            power_off_notified = False


@app.on_event("startup")
async def startup():
    asyncio.create_task(monitor())


@app.get("/ping")
async def ping():
    global last_ping
    last_ping = datetime.utcnow()
    # notify(TELEGRAM_TOKEN, chat_ids, "📶 Ping received!")
    return {"status": "ok"}