from aiogram import types


async def keyboard_choice(callback_data: str, trainings):
    buttons = []

    for training in trainings:
        button = types.InlineKeyboardButton(text=f"{training.training_time} в {training.training_day}",
                                            callback_data=f"{callback_data}_{training.id}")
        buttons.append([button])
    button_back = types.InlineKeyboardButton(text="Вернуться назад 🔙",
                                             callback_data="back_to_menu")
    buttons.append([button_back])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def keyboard_choice_admin(callback_data: str, trainings):
    buttons = []

    for training in trainings:
        button = types.InlineKeyboardButton(text=f"{training.training_time} в {training.training_day}",
                                            callback_data=f"{callback_data}_{training.id}")
        buttons.append([button])
    button_back = types.InlineKeyboardButton(text="Вернуться назад 🔙",
                                             callback_data="back_to_menu_admin")
    buttons.append([button_back])

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
