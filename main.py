import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot
from aiogram.types import Update
from bot.handlers import dp
from bot.config import TELEGRAM_TOKEN

app = FastAPI()

bot = Bot(token=TELEGRAM_TOKEN)

WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "supersecret"
WEBHOOK_URL = f"https://anekdot-bot-qraq.onrender.com{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(
        url=WEBHOOK_URL,
        secret_token=WEBHOOK_SECRET
    )
    print("Webhook set!")


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()


@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    if request.headers.get("X-Telegram-Bot-Api-Secret-Token") != WEBHOOK_SECRET:
        return {"status": "forbidden"}

    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"status": "ok"}