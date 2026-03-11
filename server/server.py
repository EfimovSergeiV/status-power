import os, asyncio, secrets
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

def getenv(name, default=None, random_len=None):
    value = os.getenv(name)

    if value:
        return value

    if random_len:
        return secrets.token_hex(random_len)

    return default


# переменные окружения
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN", random_len=16)
TELEGRAM_CHAT_ID = getenv("TELEGRAM_CHAT_ID", default="0")
PING_TIMEOUT = int(getenv("PING_TIMEOUT", default="180"))


last_ping = None
power_off_notified = False


async def monitor():
    global last_ping, power_off_notified

    while True:
        await asyncio.sleep(60)

        if last_ping is None:
            continue

        diff = (datetime.utcnow() - last_ping).total_seconds()

        if diff > PING_TIMEOUT and not power_off_notified:
            print("Power OFF")
            power_off_notified = True

        if diff <= PING_TIMEOUT and power_off_notified:
            print("Power ON")
            power_off_notified = False


@app.on_event("startup")
async def startup():
    asyncio.create_task(monitor())


@app.get("/ping")
async def ping():
    global last_ping
    last_ping = datetime.utcnow()
    return {"status": "ok"}