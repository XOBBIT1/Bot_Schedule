from aiogram import types


def keyboard_beginner():

    buttons = [
        [types.InlineKeyboardButton(text="Записаться на тренеровку", callback_data="sing_up")],
        [types.InlineKeyboardButton(text="Отменить запись", callback_data="terminate_training")],
        [types.InlineKeyboardButton(text="Ваши тренеровки", callback_data="training_list")],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def keyboard_admin():

    buttons = [
        [types.InlineKeyboardButton(text="Создать тренеровку", callback_data="create")],
        [types.InlineKeyboardButton(text="Удалить тренеровку", callback_data="delete")],
        [types.InlineKeyboardButton(text="Список не занятых тренеровок", callback_data="list_of_training")],
        [types.InlineKeyboardButton(text="Промотр людей, которые записались на тренеровку",
                                    callback_data="users_with_training")],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def back_to_menu():
    buttons = [

        [types.InlineKeyboardButton(text="Вернуться назад 🔙",
                                    callback_data="back_to_menu")],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def back_to_menu_admin():
    buttons = [

        [types.InlineKeyboardButton(text="Вернуться назад 🔙",
                                    callback_data="back_to_menu_admin")],

    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
