import os
from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.types import Update
from bot.handlers import dp
from bot.config import TELEGRAM_TOKEN

app = FastAPI()
bot = Bot(token=TELEGRAM_TOKEN)

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "supersecret"

RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")

if RENDER_URL:
    WEBHOOK_URL = RENDER_URL + WEBHOOK_PATH
else:
    WEBHOOK_URL = None
    print("❌ RENDER_EXTERNAL_URL not found")


@app.on_event("startup")
async def on_startup():
    if not WEBHOOK_URL:
        print("❌ Webhook not set (no RENDER_EXTERNAL_URL)")
        return

    try:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            secret_token=WEBHOOK_SECRET
        )
        print("✅ Webhook set:", WEBHOOK_URL)
    except Exception as e:
        print("❌ Failed to set webhook:", e)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    try:
        if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
            return {"status": "forbidden"}

        data = await request.json()
        update = Update.model_validate(data)

        await dp.feed_update(bot, update)
        return {"status": "ok"}

    except Exception as e:
        print("WEBHOOK ERROR:", e)
        return {"status": "error"}