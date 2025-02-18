from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import get_main_menu

start_router = Router()

@start_router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот для создания списка подарков.\n\n"
        "Используй кнопки ниже, чтобы управлять своим списком.",
        reply_markup=get_main_menu()
    )