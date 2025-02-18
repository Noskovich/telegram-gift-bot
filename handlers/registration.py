from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import register_user, is_user_registered
from handlers.add_link import AddLink

registration_router = Router()

class Registration(StatesGroup):
    waiting_for_username = State()

@registration_router.message(lambda message: message.text == "Добавить ссылку")
async def add_link_start(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_user_registered(user_id):
        await message.answer("Введи свое имя для регистрации:")
        await state.set_state(Registration.waiting_for_username)
    else:
        await message.answer("Отправь мне ссылку на подарок:")
        await state.set_state(AddLink.waiting_for_link)

@registration_router.message(Registration.waiting_for_username)
async def register_user_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.text
    register_user(user_id, username)
    await message.answer(f"Спасибо, {username}! Теперь ты зарегистрирован.")
    await message.answer("Отправь мне ссылку на подарок:")
    await state.set_state(AddLink.waiting_for_link)