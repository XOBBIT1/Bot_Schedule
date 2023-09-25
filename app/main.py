import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from app.settings.config_settings import token

from app.settings import logging_settings

bot = Bot(token)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging_settings.setup_logger()
    logging.info("Bot nachal rabotu !")
    asyncio.run(main())
