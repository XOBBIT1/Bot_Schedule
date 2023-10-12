from aiogram import types

from app.core.animation import loading
from app.core.keyboards.starter_keyboard import keyboard_admin, keyboard_beginner
from app.core.keyboards.trainings_keyboard import keyboard_choice
from app.core.servises.serves_training import get_all_not_booked_trainings
from aiogram.fsm.context import FSMContext

from app.core.servises.serves_user import user_trainings, sign_up_user_for_training, cancel_training
from app.core.staets.bot_state import UserState


async def sign_up_for_workout(callback: types.CallbackQuery):
    trainings = await get_all_not_booked_trainings()
    if len(trainings) == 0:
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKcsFlHWy56I5Hj"
                                                      "YqU9yR232RVaua0FAAC4AIAAvPjvguHcvn0VaCySTAE")
        await callback.message.answer("К сожалению, свободных тренерок нет!😢", parse_mode="HTML",
                                      reply_markup=keyboard_beginner())
    else:
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKe1dlIsdqF7A69iUyRXTkpx"
                                                      "RAatS59gACPhUAAvUDQUkMAAFnGZ8Jhl0wBA")
        await callback.message.answer("Тут предаставлен список 📋 <i>Тренеровок</i> \n\n "
                                      "Ты можешь <b>выбрать ТРЕНЕРОКУ НА ВЫБОР</b> "
                                      "и ты успешно запишешься на тренеровку ✅.\n\n"
                                      "<b>📋 Список тренеровок: </b>\n", parse_mode="HTML",
                                      reply_markup=await keyboard_choice("signup_button", trainings))


async def sign_up_for_training_id(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data
    training_id = callback_data.split('_')[2]
    await loading(callback.message)
    await sign_up_user_for_training(callback.message, training_id)
    await callback.message.answer("Ты успешно записался на <b>Тренеровку</b>!\n\n"
                                  "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
                                  parse_mode="HTML", reply_markup=keyboard_beginner())
    await state.update_data(name=callback.message.text)
    await state.set_state(UserState.any_text)


async def list_of_training(callback: types.CallbackQuery):
    trainings = await get_all_not_booked_trainings()
    if len(trainings) == 0:
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKcvBlHXWMECwjS"
                                                      "reQQ73Z7seMMQIbswACbxYAAg2pAUj2ZN0NwJMQIDAE")
        await callback.message.answer("Все тренеровки заняты ! 😁", parse_mode="HTML",
                                      reply_markup=keyboard_admin())
    else:
        await callback.message.answer("<b>📋 Список тренеровок: </b>\n", parse_mode="HTML")
        for training in trainings:
            await callback.message.answer(f"<b>{training.id}.</b>"
                                          f" <i>{training.training_day} {training.training_time}</i>",
                                          parse_mode="HTML")
        await callback.message.answer(
            "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
            parse_mode="HTML", reply_markup=keyboard_admin())


async def all_user_trainings(callback: types.CallbackQuery):
    trainings = await user_trainings(callback.message)
    if len(trainings) == 0:
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKcsFlHWy56I5Hj"
                                                      "YqU9yR232RVaua0FAAC4AIAAvPjvguHcvn0VaCySTAE")
        await callback.message.answer("Выпока ещё не записались на тренеровку😢", parse_mode="HTML",
                                      reply_markup=keyboard_beginner())
    else:
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKe1llIsgsUA54olWoLwABjRT2"
                                                      "momWoZUAAgQbAAJ1akFJMxhpFcprXMkwBA")
        await callback.message.answer("<b>📋 Список твоих тренеровок: </b>\n", parse_mode="HTML")
        for training in trainings:
            await callback.message.answer(
                f"<i>{training.training_day} {training.training_time}</i>",
                parse_mode="HTML")
        await callback.message.answer(
            "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
            parse_mode="HTML", reply_markup=keyboard_beginner())


async def cancel_user_training(callback: types.CallbackQuery):
    trainings = await user_trainings(callback.message)
    if len(trainings) == 0:
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKcr1lHWxfr-ggwpK_"
                                                      "FtjDAatB01J2bQACGwMAArrAlQWa_UGAaJawejAE")
        await callback.message.answer("Вам пока нечего отменять 🤷‍♂️", parse_mode="HTML",
                                      reply_markup=keyboard_beginner())
    else:
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKe1NlIsalusmAf_"
                                                      "MM3DwUuJtY3XtmZwACDg0AAlkAAZhL3larpAvx_n8wBA")
        await callback.message.answer("Выбери, какую тренероку нужно отменить.\n\n"
                                      "<b>📋 Список твоих тренеровок: </b>\n", parse_mode="HTML",
                                      reply_markup=await keyboard_choice("terminate_button", trainings))


async def terminate_training(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data
    training_id = callback_data.split('_')[2]
    await loading(callback.message)
    await cancel_training(callback.message, training_id)
    await callback.message.answer("Ты успешно отменил запись на <b>Тренеровку</b>!\n\n"
                                  "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
                                  parse_mode="HTML", reply_markup=keyboard_beginner())
    await state.set_state(UserState.any_text)
