from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.message(commands=["start"])
async def cmd_start(message: types.Message):
    await send_main_menu(message)

async def send_main_menu(message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📈 Графіки", callback_data="menu_graphs")],
        [InlineKeyboardButton(text="⚙️ Пороги", callback_data="menu_thresholds")],
        [InlineKeyboardButton(text="📁 Вивантаження логів", callback_data="menu_logs")],
        [InlineKeyboardButton(text="🛠️ Налаштування", callback_data="menu_settings")],
        [InlineKeyboardButton(text="👑 Адмін панель", callback_data="menu_admin")]
    ])
    await message.answer("Головне меню:", reply_markup=keyboard)