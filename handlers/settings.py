from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

router = Router()

@router.callback_query(lambda c: c.data == "menu_settings")
async def show_settings(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Мова: 🇺🇦", callback_data="lang_ua"),
         InlineKeyboardButton(text="Language: 🇬🇧", callback_data="lang_en")],
        [InlineKeyboardButton(text="Частота: 15 хв", callback_data="freq_15"),
         InlineKeyboardButton(text="30 хв", callback_data="freq_30"),
         InlineKeyboardButton(text="1 год", callback_data="freq_60")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back")]
    ])
    await callback.message.edit_text("Налаштування:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("lang_") or c.data.startswith("freq_"))
async def save_setting(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    setting_type, value = callback.data.split("_")
    os.makedirs("bot/data", exist_ok=True)
    settings = {}
    try:
        with open("bot/data/user_settings.json", encoding="utf-8") as f:
            settings = json.load(f)
    except:
        pass
    if user_id not in settings:
        settings[user_id] = {}
    settings[user_id][setting_type] = value
    with open("bot/data/user_settings.json", "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
    await callback.answer("Налаштування збережено")