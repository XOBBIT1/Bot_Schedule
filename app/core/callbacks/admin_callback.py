from aiogram import types
from aiogram.fsm.context import FSMContext

from app.core.keyboards.starter_keyboard import keyboard_admin, back_to_menu_admin
from app.core.keyboards.trainings_keyboard import keyboard_choice_admin
from app.core.servises.serves_training import get_all_trainings, \
    checking_users_with_trainings, delete_training_by_id
from app.core.staets.bot_state import AdminState


async def create_training_week_day(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKe1dlIsdqF7A69iUyRXTkpx"
                                                  "RAatS59gACPhUAAvUDQUkMAAFnGZ8Jhl0wBA")
    await callback.message.answer("Введи <i>день недели 🗓</i> \n\n "
                                  "Привер: <b><i>Понедельник</i></b>", parse_mode="HTML",
                                  reply_markup=back_to_menu_admin())
    await state.set_state(AdminState.week_day)


async def delete_training(message: types.Message):
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
                             "Ты можешь <b>выбрать ТРЕНЕРОКУ НА ВЫБОР</b>"
                             "и данная тренеровка будет удалина.\n\n"
                             "<b>📋 Список тренеровок: </b>\n", parse_mode="HTML",
                             reply_markup=await keyboard_choice_admin("delete_button", trainings)
                             )


async def check_users(message: types.Message):
    trainings = await checking_users_with_trainings()
    if len(trainings) == 0:
        await message.answer_sticker(sticker="CAACAgIAAxkBAAEKcsFlHWy56I5Hj"
                                             "YqU9yR232RVaua0FAAC4AIAAvPjvguHcvn0VaCySTAE")
        await message.answer("Пока никто не записался!😢", parse_mode="HTML",
                             reply_markup=keyboard_admin())
    else:
        await message.answer_sticker(sticker="CAACAgIAAxkBAAEKe25lIsnQb5sXWhnDiW49L"
                                             "__DFaHQCwACUhMAAkSLAAFIc7Llet9uhRwwBA")
        for training in trainings:
            user = training.user
            await message.answer(f"<b>{user.user_name}</b> занял тренеровку: \n"
                                 f"<i>{training.training_day} {training.training_time}</i>",
                                 parse_mode="HTML")
        await message.answer(
            "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
            parse_mode="HTML", reply_markup=keyboard_admin())


async def delete_by_training_id(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data
    training_id = callback_data.split('_')[2]
    await delete_training_by_id(training_id)
    await callback.message.answer(
        "<b>Тренеровка была удалена!</b>\n\n"
        "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
        parse_mode="HTML", reply_markup=keyboard_admin())
    await state.set_state(AdminState.new_menu_delete)
