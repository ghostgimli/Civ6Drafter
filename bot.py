# bot.py
import logging

 # токен из config.py


import logging
from dotenv import dotenv_values
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import draft
# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)

config = dotenv_values("vars.env")

logging.basicConfig(level=logging.ERROR)

bot = Bot(token=config['TGBOT_TOKEN'])
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Hello! I am Civ6 Drafter. For starting a draft enter the /draft command"
    )

# @dp.message()
# async def echo(message: types.Message):
#     await message.answer(f"Ты написал: {message.text}")


if __name__ == "__main__":
    dp.include_router(draft.router)
    dp.run_polling(bot)
# Логирование (полезно для отладки)