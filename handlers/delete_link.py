from aiogram import Router, types
from database import delete_link, get_user_links
from keyboards.main_menu import get_main_menu

delete_link_router = Router()

@delete_link_router.message(lambda message: message.text.startswith("/delete"))
async def delete_link_handler(message: types.Message):
    user_id = message.from_user.id
    link = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None

    if not link:
        await message.answer("Используй: /delete [ссылка]")
        return

    delete_link(user_id, link)
    await message.answer(f'Ссылка "{link}" удалена из твоего списка!')

@delete_link_router.message(lambda message: message.text == "Посмотреть весь список")
async def get_all_links_handler(message: types.Message):
    user_id = message.from_user.id
    links = get_user_links(user_id)
    if links:
        await message.answer(f"Твой список:\n" + "\n".join(links))
    else:
        await message.answer("Твой список пока пуст.")