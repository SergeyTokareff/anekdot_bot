from aiogram import Dispatcher, F
from aiogram.filters import Command
from aiogram import types
from bot.ai_service import generate_joke
from bot.limits_service import can_get_joke

dp = Dispatcher()


@dp.message(Command("anekdot"))
async def handle_anekdot(message: types.Message):
    if not can_get_joke(message.from_user.id):
        await message.bot.send_message(
            message.from_user.id,
            "😅 Ти вже сьогодні отримав анекдот. Приходь завтра!"
        )
        return

    try:
        joke = await generate_joke()
    except Exception as e:
        joke = "🤖 Не вдалося отримати анекдот."
        print(e)

    await message.reply(joke)

# --- Реакція на команду /anekdot ---
@dp.message(Command("anekdot"))
async def handle_command(message: types.Message):
    await handle_anekdot(message)


# --- Реакція на будь-яке повідомлення, де є слово "анекдот" ---
@dp.message(F.text)
async def handle_text(message: types.Message):
    text = message.text.lower()
    if "анекдот" in text:
        await handle_anekdot(message)