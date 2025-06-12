from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_answer import CallbackAnswer
import matplotlib.pyplot as plt
import json
import io

router = Router()
SECTIONS = ["розкрій", "армування", "зварювання", "зачистка", "скління", "контроль"]

@router.callback_query(lambda c: c.data == "menu_graphs")
async def show_graphs_menu(callback: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=section, callback_data=f"graph_{section}")]
        for section in SECTIONS
    ] + [[InlineKeyboardButton(text="⬅️ Назад", callback_data="go_back")]])
    await callback.message.edit_text("Оберіть ділянку для перегляду графіка:", reply_markup=keyboard)

@router.callback_query(lambda c: c.data.startswith("graph_"))
async def show_graph(callback: types.CallbackQuery):
    section = callback.data.split("_", 1)[1]
    with open("bot/data/storage.json", encoding="utf-8") as f:
        data = json.load(f)

    section_data = data.get(section, {"вироблені_одиниці": 0})
    y = [section_data["вироблені_одиниці"] + i*5 for i in range(10)]

    plt.figure()
    plt.plot(range(10), y)
    plt.title(f"Ділянка: {section}")
    plt.xlabel("Час")
    plt.ylabel("Одиниці")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    await callback.message.answer_photo(photo=buf, caption=f"Графік для {section}")
    await show_graphs_menu(callback)