import time
from aiogram import types

from app.settings.config_settings import bot


async def loading(message: types.Message):
    load = "Загрузка: {}"
    sent_message = await message.answer(load.format("⏳"))

    for i in range(2, 7):
        time.sleep(1)
        updated_text = load.format("⏳" * i)
        updated_text += " "
        await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id, text=updated_text)
