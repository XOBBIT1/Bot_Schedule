import asyncio
import logging

from aiogram import Bot, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from app.core.bot_commands.commands import starter, for_coach, ask_name, dop_starter, create_training_time_of_training, \
    new_admin_menu, delete_by_training_id, sign_up_for_training_id, terminate_training
from app.core.callbacks.admin_callback import delete_training, create_training_week_day, check_users
from app.core.callbacks.starter_callback import sign_up_for_workout, list_of_training, all_user_trainings, \
    cancel_user_training
from app.core.staets.bot_state import UserState, AdminState
from app.settings.config_settings import token, dp, router

from app.settings import logging_settings

bot = Bot(token)


# Commands
@router.message(Command("start"))
async def cmd_user_name(message: types.Message, state: FSMContext):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEKagllFsZWSE8dS8mOFHf-iezTnZHbTgACJwMAArVx2gYP9N7PoMXd7DAE")
    await ask_name(message, state)


@router.message(UserState.waiting_for_name)
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEKaYllFpQlys_r556Y87Gt5EcflHwEWwACAw4AAoRT4EuHFN5qbTL60jAE")
    await starter(message, state)


@dp.message(Command("admin"))
async def cmd_coach(message: types.Message):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEKZXhlExevM5_3kQyd7rnXBNRuoMt1bAACZBQAAjzxyEuwdKvRZVMPlzAE")
    await for_coach(message)


@router.message(UserState.any_text)
async def cmd_dop_start(message: types.Message):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEKaY1lFpQwGVqgWv0ivQQpp5kWS3fWMwACDwMAAvPjvgtTO-Z7BumZjjAE")
    await dop_starter(message)


@router.message(UserState.sign_up_for_training)
async def cmd_successfully_sign_up(message: types.Message, state: FSMContext):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEKcQtlHBAnYmCMR602x_6VJ6_DND3BswACJgMAArVx2gY-GQuL5xwZQDAE")
    await sign_up_for_training_id(message, state)


@router.message(UserState.cancel_training_for_user)
async def cmd_cancel_training(message: types.Message, state: FSMContext):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEKcQtlHBAnYmCMR602x_6VJ6_DND3BswACJgMAArVx2gY-GQuL5xwZQDAE")
    await terminate_training(message, state)


@router.message(AdminState.week_day)
async def cmd_create_training_time(message: types.Message, state: FSMContext):
    await create_training_time_of_training(message, state)


@router.message(AdminState.time_of_training)
async def cmd_create_training_new_menu(message: types.Message, state: FSMContext):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEKcQtlHBAnYmCMR602x_6VJ6_DND3BswACJgMAArVx2gY-GQuL5xwZQDAE")
    await new_admin_menu(message, state)


@router.message(AdminState.delete_training_id)
async def cmd_delete_training_new_menu(message: types.Message, state: FSMContext):
    await message.answer_sticker(sticker="CAACAgIAAxkBAAEKcQtlHBAnYmCMR602x_6VJ6_DND3BswACJgMAArVx2gY-GQuL5xwZQDAE")
    await delete_by_training_id(message, state)


# Callbacks
@router.callback_query(F.data == "sing_up")
async def callback_beginner(callback: types.CallbackQuery, state: FSMContext):
    await sign_up_for_workout(callback, state)


@router.callback_query(F.data == "training_list")
async def callback_trainings_list(callback: types.CallbackQuery):
    await all_user_trainings(callback)


@router.callback_query(F.data == "delete")
async def callback_delete_training(callback: types.CallbackQuery, state: FSMContext):
    await delete_training(callback.message, state)


@router.callback_query(F.data == "list_of_training")
async def callback__user_trainings_list(callback: types.CallbackQuery):
    await list_of_training(callback)


@router.callback_query(F.data == "create")
async def callback_create_training_week_day(callback: types.CallbackQuery, state: FSMContext):
    await create_training_week_day(callback, state)


@router.callback_query(F.data == "users_with_training")
async def callback_check_user(callback: types.CallbackQuery):
    await check_users(callback.message)


@router.callback_query(F.data == "terminate_training")
async def callback_checking_user(callback: types.CallbackQuery, state: FSMContext):
    await cancel_user_training(callback, state)


@router.callback_query(F.data == "back_to_menu")
async def callback_back_to_menu_starter(callback: types.CallbackQuery):
    await dop_starter(callback.message)


@router.callback_query(F.data == "back_to_menu_admin")
async def callback_back_to_menu_admin(callback: types.CallbackQuery):
    await for_coach(callback.message)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging_settings.setup_logger()
    logging.info("Bot nachal rabotu !")
    dp.include_router(router)
    asyncio.run(main())
