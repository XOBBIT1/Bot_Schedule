import time

import telebot
from app.settings.config_settings import token

bot = telebot.TeleBot(token, parse_mode='html')


def loading(message, string, icon):
    load = string
    wait = bot.send_message(message.chat.id, load.format(f' {icon}'))
    for i in range(2, 7):
        time.sleep(1)
        bot.edit_message_text(load.format(f' {icon * i}'), message.chat.id, wait.message_id)


def get_sticker(message, name_of_file):
    sticker = bot.send_sticker(message.chat.id, open(f"static/{name_of_file}", "rb"))
    return sticker
