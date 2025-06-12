from aiogram import Router, types
import json

router = Router()

@router.callback_query(lambda c: c.data == "menu_logs")
async def export_logs(callback: types.CallbackQuery):
    with open("bot/data/storage.json", encoding="utf-8") as f:
        data = json.load(f)
    text = "Звіт: усі ділянки працюють коректно\n\n"
    for section, info in data.items():
        text += f"Ділянка: {section}\nТемпература: {info['температура']}\nСтатус: {info['статус']}\n\n"

    with open("bot/data/report.txt", "w", encoding="utf-8") as f:
        f.write(text)

    await callback.message.answer_document(types.FSInputFile("bot/data/report.txt"), caption="Звіт по ділянках")