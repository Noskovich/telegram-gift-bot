from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from database import get_random_link, get_user_links
from keyboards.main_menu import get_user_actions_keyboard, get_main_menu, get_users_keyboard

gift_idea_router = Router()

@gift_idea_router.message(lambda message: message.text == "Идея для подарка")
async def gift_idea_start(message: types.Message):
    await message.answer("Выбери пользователя:", reply_markup=get_users_keyboard())

@gift_idea_router.callback_query(lambda callback: callback.data.startswith("user_"))
async def handle_user_selection(callback: types.CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[1])
    await state.update_data(selected_user_id=user_id)
    await callback.message.answer(
        "Что ты хочешь сделать?",
        reply_markup=get_user_actions_keyboard()
    )
    await callback.answer()

@gift_idea_router.message(lambda message: message.text == "Получить случайную ссылку")
async def get_random_link_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    selected_user_id = data.get("selected_user_id")
    if not selected_user_id:
        await message.answer("Сначала выбери пользователя.")
        return

    random_link = get_random_link(selected_user_id)
    if random_link:
        await message.answer(f"Вот случайная ссылка: {random_link}")
    else:
        await message.answer("У этого пользователя пока нет списка подарков.")

@gift_idea_router.message(lambda message: message.text == "Посмотреть весь список")
async def get_all_links_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    selected_user_id = data.get("selected_user_id")
    if not selected_user_id:
        await message.answer("Сначала выбери пользователя.")
        return

    links = get_user_links(selected_user_id)
    if links:
        await message.answer(f"Весь список:\n" + "\n".join(links))
    else:
        await message.answer("У этого пользователя пока нет списка подарков.")

@gift_idea_router.message(lambda message: message.text == "Главное меню")
async def back_to_menu(message: types.Message):
    await message.answer("Возвращаюсь в главное меню.", reply_markup=get_main_menu())