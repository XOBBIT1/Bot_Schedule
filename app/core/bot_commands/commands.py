from aiogram import types
from aiogram.fsm.context import FSMContext

from app.core.keyboards.starter_keyboard import keyboard_beginner, keyboard_admin, back_to_menu_admin
from app.core.servises.serves_user import create_user, get_user_name, sign_up_user_for_training, cancel_training, \
    check_user
from app.core.servises.serves_training import create_training, delete_training_by_id
from app.core.staets.bot_state import UserState, AdminState

create_training_dict = {}


async def ask_name(message: types.Message, state: FSMContext):
    user = await check_user(message)
    if user > 0:
        await state.set_state(UserState.any_text)
        await message.answer(f"Привет <b>{await get_user_name(message)}</b>! 👋\n\n"
                             f"Рад тебя снова видете !!!\n"
                             f"<b>Жми на интересующее тебя поля ниже👇 и продолжай прокачивать себя 🦾</b>\n\n"
                             f"УДАЧИ !!!", parse_mode="HTML", reply_markup=keyboard_beginner())
    else:
        await state.set_state(UserState.waiting_for_name)
        await message.answer("Привет! Как тебя зовут?")


async def starter(message: types.Message, state: FSMContext):
    await create_user(message, message.text)
    await message.answer(f"Привет <b>{message.text}</b>!\n\n"
                         f"Добро пожаловать, в бота для рассписания тренеровок📋.\n\n"
                         f"<b>Хочешь стать по истене Железным человеком ?🦾🦾🦾</b>\n\n"
                         f"Тогда <b>Жми на кнопку 'Записаться на тренеровку'</b>👇 и "
                         f"начинай свой путь 🛣...\n\n"
                         f"Если потеряешь главное меню, то просто напиши мне\n"
                         f"и я сразу отвечу тебе) 😉", parse_mode="HTML", reply_markup=keyboard_beginner())
    await state.update_data(name=message.text)
    await state.set_state(UserState.any_text)


async def dop_starter(message: types.Message):
    await message.answer(f"Привет <b>{await get_user_name(message)}</b>! 👋\n\n"
                         f"Рад тебя снова видете !!!\n"
                         f"<b>Жми на интересующее тебя поля ниже👇 и продолжай прокачивать себя 🦾</b>\n\n"
                         f"УДАЧИ !!!", parse_mode="HTML", reply_markup=keyboard_beginner())


async def for_coach(message: types.Message):
    await message.answer(
        "Приветствую <b>Данджен мастера</b> данного заведения\n\n"
        "Здесь ты можешь:\n"
        " 🏀️ <i>Создать тренеровку. <b>Тут ты указываешь время тренеровки и день недели!</b></i>\n"
        " 🏐 <i>Удалить тренеровку, если, допустим, ты решил поменять Время.</i>\n"
        " 🎾 <i>Список не занятых тренеровок</i>\n"
        " 🏉 <i>Промотр людей, которые записались на тренеровку</i>\n\n"
        "Надеюсь твои ученики не будут молить о пощаде после первой тренировки.",
        parse_mode="HTML", reply_markup=keyboard_admin()
    )


async def create_training_time_of_training(message: types.Message, state: FSMContext):
    await state.update_data(week_day=message.text)
    await message.answer("Введи <i>Время Тренеровки</i> \n\n "
                         "Пример: <b><i>12:45</i></b>", parse_mode="HTML", reply_markup=back_to_menu_admin())
    await state.set_state(AdminState.time_of_training)


async def new_admin_menu(message: types.Message, state: FSMContext):
    data = await state.update_data(time_of_training=message.text)
    await create_training(data['week_day'], data['time_of_training'])
    await message.answer(
        f"<b>Тренеровка в <i>{data['week_day']} в {data['time_of_training']}</i> успешно созданна!</b>\n\n"
        "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
        parse_mode="HTML", reply_markup=keyboard_admin())
    await state.set_state(AdminState.new_menu_create)


async def delete_by_training_id(message: types.Message, state: FSMContext):
    data = await state.update_data(training_id=message.text)
    await delete_training_by_id(data['training_id'])
    await message.answer(
        f"<b>Тренеровка <i>{data['training_id']}</i> была удалена!</b>\n\n"
        "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
        parse_mode="HTML", reply_markup=keyboard_admin())
    await state.set_state(AdminState.new_menu_delete)


async def sign_up_for_training_id(message: types.Message, state: FSMContext):
    data = await state.update_data(training_id=message.text)
    await sign_up_user_for_training(message, data['training_id'])
    await message.answer("Ты успешно записался на <b>Тренеровку</b>!\n\n"
                         "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
                         parse_mode="HTML", reply_markup=keyboard_beginner())
    await state.update_data(name=message.text)
    await state.set_state(UserState.any_text)


async def terminate_training(message: types.Message, state: FSMContext):
    data = await state.update_data(training_id=message.text)
    await cancel_training(message, data['training_id'])
    await message.answer("Ты успешно отменил запись на <b>Тренеровку</b>!\n\n"
                         "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
                         parse_mode="HTML", reply_markup=keyboard_beginner())
    await state.set_state(UserState.any_text)
