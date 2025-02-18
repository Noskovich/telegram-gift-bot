from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_link_to_db
from keyboards.main_menu import get_after_add_keyboard, get_main_menu
from urllib.parse import urlparse

add_link_router = Router()

class AddLink(StatesGroup):
    waiting_for_link = State()

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

@add_link_router.message(AddLink.waiting_for_link)
async def add_link_finish(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    link = message.text
    if not is_valid_url(link):
        await message.answer("Это не похоже на ссылку. Попробуй еще раз.")
        return

    
    add_link_to_db(user_id, link)
    await message.answer(
        f'Ссылка "{link}" добавлена в твой список!',
        reply_markup=get_after_add_keyboard()
    )
    await state.clear()

@add_link_router.message(lambda message: message.text == "Добавить еще")
async def add_more(message: types.Message, state: FSMContext):
    await message.answer("Отправь мне следующую ссылку:")
    await state.set_state(AddLink.waiting_for_link)

@add_link_router.message(lambda message: message.text == "Главное меню")
async def back_to_menu(message: types.Message):
    await message.answer("Возвращаюсь в главное меню.", reply_markup=get_main_menu())