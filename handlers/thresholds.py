from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import os

router = Router()
SECTIONS = ["розкрій", "армування", "зварювання", "зачистка", "скління", "контроль"]

class ThresholdState(StatesGroup):
    waiting_for_value = State()

selected_section = {}

@router.callback_query(lambda c: c.data == "menu_thresholds")
async def thresholds_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=section, callback_data=f"set_threshold_{section}")]
        for section in SECTIONS
    ] + [[InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back")]])
    await callback.message.edit_text("Оберіть ділянку для встановлення порогу:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("set_threshold_"))
async def ask_threshold(callback: types.CallbackQuery, state: FSMContext):
    section = callback.data.split("_")[-1]
    selected_section[callback.from_user.id] = section
    await callback.message.answer(f"Введіть числове значення порогу для {section}:")
    await state.set_state(ThresholdState.waiting_for_value)

@router.message(ThresholdState.waiting_for_value)
async def save_threshold(message: types.Message, state: FSMContext):
    section = selected_section.get(message.from_user.id)
    value = message.text
    if not value.isdigit():
        await message.answer("Будь ласка, введіть число.")
        return
    os.makedirs("bot/data", exist_ok=True)
    thresholds = {}
    try:
        with open("bot/data/thresholds.json", encoding="utf-8") as f:
            thresholds = json.load(f)
    except:
        pass
    thresholds[section] = int(value)
    with open("bot/data/thresholds.json", "w", encoding="utf-8") as f:
        json.dump(thresholds, f, ensure_ascii=False, indent=2)
    await message.answer(f"Поріг для {section} встановлено на {value}.")
    await state.clear()