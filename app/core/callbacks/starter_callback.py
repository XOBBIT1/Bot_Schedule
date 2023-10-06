import logging

from aiogram import types

from app.core.keyboards.starter_keyboard import keyboard_admin, keyboard_beginner, back_to_menu
from app.core.servises.serves_training import get_all_not_booked_trainings
from aiogram.fsm.context import FSMContext

from app.core.servises.serves_user import user_trainings
from app.core.staets.bot_state import UserState


async def sign_up_for_workout(callback: types.CallbackQuery, state: FSMContext):
    trainings = await get_all_not_booked_trainings()
    if len(trainings) == 0:
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKcsFlHWy56I5Hj"
                                                      "YqU9yR232RVaua0FAAC4AIAAvPjvguHcvn0VaCySTAE")
        await callback.message.answer("К сожалению, свободных тренерок нет!😢", parse_mode="HTML",
                                      reply_markup=keyboard_beginner())
    else:
        for training in trainings:
            logging.info(training)
            if training:
                await callback.message.answer("Тут предаставлен список 📋 <i>Тренеровок</i> \n\n "
                                              "Ты можешь <b>выбрать ПОРЯДКОВЫЙ</b> НОМЕР любой из тренеровок"
                                              "и ты успешно запишешься на тренеровку ✅.\n\n", parse_mode="HTML",
                                              reply_markup=back_to_menu()
                                              )
                await callback.message.answer(
                    f"<b>📋 Список тренеровок: </b>\n"
                    f"<b>{training.id}.</b> <i>{training.training_day} {training.training_time}</i>",
                    parse_mode="HTML")
        await callback.message.answer("<i>Пример как записаться:\n 2. Понедельник 12:30\n\n "
                                      "Вводим <b>2</b></i>", parse_mode="HTML")
        await state.set_state(UserState.sign_up_for_training)


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
            await callback.message.answer(f"<b>{training.id}.</b> <i>{training.training_day} {training.training_time}</i>",
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
        await callback.message.answer("<b>📋 Список твоих тренеровок: </b>\n", parse_mode="HTML")
        for training in trainings:
            await callback.message.answer(
                f"<b>{training.id}.</b> <i>{training.training_day} {training.training_time}</i>",
                parse_mode="HTML")
        await callback.message.answer(
            "Если тебе захочется сделать другие манипуляции, то список снизу 👇\n\n",
            parse_mode="HTML", reply_markup=keyboard_beginner())


async def cancel_user_training(callback: types.CallbackQuery, state: FSMContext):
    trainings = await user_trainings(callback.message)
    if len(trainings) == 0:
        await callback.message.answer_sticker(sticker="CAACAgIAAxkBAAEKcr1lHWxfr-ggwpK_"
                                                      "FtjDAatB01J2bQACGwMAArrAlQWa_UGAaJawejAE")
        await callback.message.answer("Вам пока нечего отменять 🤷‍♂️", parse_mode="HTML",
                                      reply_markup=keyboard_beginner())
    else:
        await callback.message.answer("Выбери, какую тренероку нужно отменить.\n\n"
                                      "<b>📋 Список твоих тренеровок: </b>\n", parse_mode="HTML",
                                      reply_markup=back_to_menu())
        for training in trainings:
            await callback.message.answer(f"<b>{training.id}.</b> <i>{training.training_day} {training.training_time}</i>",
                                          parse_mode="HTML")
        await callback.message.answer("<i>Пример как отменить запись:\n 2. Понедельник 12:30\n\n "
                                      "Вводим <b>2</b></i>", parse_mode="HTML")
        await state.set_state(UserState.cancel_training_for_user)
