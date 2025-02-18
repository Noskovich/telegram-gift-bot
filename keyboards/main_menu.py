from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Основное меню
def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить ссылку")],
            [KeyboardButton(text="Идея для подарка")]
        ],
        resize_keyboard=True
    )

# Кнопки после добавления ссылки
def get_after_add_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Добавить еще")],
            [KeyboardButton(text="Главное меню")]
        ],
        resize_keyboard=True
    )

# Кнопки после выбора пользователя
def get_user_actions_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Получить случайную ссылку")],
            [KeyboardButton(text="Посмотреть весь список")],
            [KeyboardButton(text="Главное меню")]
        ],
        resize_keyboard=True
    )

# Inline-кнопки с именами пользователей
def get_users_keyboard():
    from database import get_all_users
    users = get_all_users()
    keyboard = []
    for user in users:
        button = InlineKeyboardButton(text=user['username'], callback_data=f"user_{user['user_id']}")
        keyboard.append([button])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)