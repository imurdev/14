from aiogram import Router, types
import json
import os

router = Router()
ADMIN_ID = 123456789  # замініть на ваш Telegram ID

@router.callback_query(lambda c: c.data == "menu_admin")
async def admin_panel(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("Доступ заборонено", show_alert=True)
        return
    await callback.message.answer("Введіть ID користувача для додавання:")

@router.message()
async def handle_admin_input(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    if not message.text.isdigit():
        await message.answer("Будь ласка, введіть числовий ID.")
        return
    user_id = message.text
    os.makedirs("bot/data", exist_ok=True)
    try:
        with open("bot/data/authorized_users.json", encoding="utf-8") as f:
            users = json.load(f)
    except:
        users = []
    if user_id not in users:
        users.append(user_id)
    with open("bot/data/authorized_users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False)
    await message.answer(f"Користувача {user_id} додано.")