import os
import asyncio
import secrets
import httpx
from fastapi import FastAPI
from datetime import datetime, timezone
from contextlib import asynccontextmanager


def getenv(name, default=None):
    value = os.getenv(name)
    if value:
        return value
    if default:
        return default
    raise RuntimeError(f"{name} not set")


TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")
PING_TIMEOUT = int(getenv("PING_TIMEOUT", "180"))


class AppState:

    def __init__(self):
        self.last_ping: datetime | None = None
        self.power_off_notified = False
        self.chat_ids = set()
        self.last_update_id = 0
        self.stop_event = asyncio.Event()


state = AppState()


async def notify(client, text):

    for chat_id in state.chat_ids:

        try:
            await client.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text
                }
            )

        except Exception as e:
            print("notify error:", e)


async def telegram_polling(client):

    while not state.stop_event.is_set():

        try:

            resp = await client.get(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates",
                params={
                    "offset": state.last_update_id + 1,
                    "timeout": 30
                },
                timeout=35
            )

            data = resp.json()

            for update in data.get("result", []):

                state.last_update_id = update["update_id"]

                msg = update.get("message")
                if not msg:
                    continue

                chat = msg.get("chat")
                state.chat_ids.add(chat["id"])

        except Exception as e:
            print("telegram polling error:", e)
            await asyncio.sleep(5)


async def monitor(client):

    while not state.stop_event.is_set():

        await asyncio.sleep(60)

        if state.last_ping is None:
            continue

        diff = (datetime.now(timezone.utc) - state.last_ping).total_seconds()

        if diff > PING_TIMEOUT and not state.power_off_notified:

            print("Power OFF")

            await notify(client, "⚠️ Power OFF detected!")
            state.power_off_notified = True

        if diff <= PING_TIMEOUT and state.power_off_notified:

            print("Power ON")

            await notify(client, "✅ Power ON detected!")
            state.power_off_notified = False


@asynccontextmanager
async def lifespan(app: FastAPI):

    client = httpx.AsyncClient()

    poll_task = asyncio.create_task(telegram_polling(client))
    monitor_task = asyncio.create_task(monitor(client))

    yield

    state.stop_event.set()

    poll_task.cancel()
    monitor_task.cancel()

    await client.aclose()


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
async def ping():

    state.last_ping = datetime.now(timezone.utc)

    return {"status": "ok"}