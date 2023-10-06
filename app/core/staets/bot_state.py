from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    waiting_for_name = State()
    any_text = State()
    sign_up_for_training = State()
    cancel_training_for_user = State()


class AdminState(StatesGroup):
    time_of_training = State()
    week_day = State()
    new_menu_create = State()
    new_menu_delete = State()
    delete_training_id = State()
