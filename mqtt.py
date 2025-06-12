import asyncio
import random
import json
import os

SECTION_NAMES = ["розкрій", "армування", "зварювання", "зачистка", "скління", "контроль"]

async def simulate_mqtt():
    while True:
        data = {}
        for section in SECTION_NAMES:
            data[section] = {
                "температура": round(random.uniform(18.0, 25.0), 2),
                "статус": random.choice(["ОК", "ПОМИЛКА", "ЗУПИНКА"]),
                "вироблені_одиниці": random.randint(50, 200)
            }

        os.makedirs("bot/data", exist_ok=True)
        with open("bot/data/storage.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        await asyncio.sleep(10)