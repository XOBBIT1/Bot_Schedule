from aiogram import types
from aiogram.fsm.context import FSMContext

from app.core.keyboards.starter_keyboard import keyboard_admin, back_to_menu_admin
from app.core.servises.serves_training import get_all_trainings, \
    checking_users_with_trainings
from app.core.staets.bot_state import AdminState


async def create_training_week_day(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введи <i>день недели 🗓</i> \n\n "
                                  "Привер: <b><i>Понедельник</i></b>", parse_mode="HTML",
                                  reply_markup=back_to_menu_admin())
    await state.set_state(AdminState.week_day)


async def delete_training(message: types.Message, state: FSMContext):
    trainings = await get_all_trainings()
    if len(trainings) == 0:
        await message.answer_sticker(sticker="CAACAgIAAxkBAAEKcr1lHWxfr-ggwpK_"
                                             "FtjDAatB01J2bQACGwMAArrAlQWa_UGAaJawejAE")
        await message.answer("Вам пока нечего удалять 🤷‍♂️", parse_mode="HTML",
                             reply_markup=keyboard_admin())
    else:
        await message.answer_sticker(sticker="CAACAgIAAxkBAAEKcQ1lHBEVm8vAKYvST5yATZqjKjkc"
                                             "JAACaQkAAhhC7gia--ItXVObQjAE")
        await message.answer("Тут предаставлен список<i>Созданных Тренеровок</i> \n\n "
                             "Ты можешь <b>выбрать ПОРЯДКОВЫЙ</b> НОМЕР любой из тренеровок"
                             "и данная тренеровка будет удалина.\n\n"
                             "<b>📋 Список тренеровок: </b>\n", parse_mode="HTML", reply_markup=back_to_menu_admin()
                             )
        for training in trainings:
            await message.answer(f"<b>{training.id}.</b> <i>{training.training_day} {training.training_time}</i>",
                                 parse_mode="HTML")
        await message.answer("<i>Пример как удалять:\n 2. Понедельник 12:30\n\n "
                             "Вводим <b>2</b></i>", parse_mode="HTML")
        await state.set_state(AdminState.delete_training_id)


async def check_users(message: types.Message):
    trainings = await checking_users_with_trainings()
    if len(trainings) == 0:
        await message.answer_sticker(sticker="CAACAgIAAxkBAAEKcsFlHWy56I5Hj"
                                             "YqU9yR232RVaua0FAAC4AIAAvPjvguHcvn0VaCySTAE")
        await message.answer("Пока никто не записался!😢", parse_mode="HTML",
                             reply_markup=keyboard_admin())
    else:
        for training in trainings:
            user = training.user
            await message.answer(f"<b>{user.user_name}</b> занял тренеровку: \n"
                                 f"<i>{training.training_day} {training.training_time}</i>",
                                 parse_mode="HTML")
        await message.answer(
            "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
            parse_mode="HTML", reply_markup=keyboard_admin())
