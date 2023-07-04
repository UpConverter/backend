import asyncio
from src.data.fill_database import fill_database

data = {
    "DeviceType": [
        {"name": "SA"},
        {"name": "CAL"},
        {"name": "UPCONVERTER"}
    ],
    "DeviceModel": [
        {"name": "COAXIAL"},
        {"name": "SOLID STATE"}
    ],
    "DeviceState": [
        {"name": "CRYO"},
        {"name": "CAL"},
        {"name": "TERMINATE"}
    ],
    "DeviceAdditionalState": [
        {"name": "LO_FULL"},
        {"name": "LO_SPLIT"},
    ],
    "Channel": [
        {"name": "CH1"},
        {"name": "CH2"},
        {"name": "CH3"},
        {"name": "CH4"},
        {"name": "CH5"},
        {"name": "CH6"},
    ],
    "Speed": [
        {"value": 57600},
        {"value": 256000},
        {"value": 115200},
        {"value": 921600}
    ],
    "Port": [
        {"name": "COM1"},
        {"name": "COM2"},
        {"name": "COM3"},
        {"name": "COM4"},
    ],
}

# Вызов функции заполнения базы данных при необходимости
async def main():
    await fill_database(data)

# Запуск сопрограммы
asyncio.run(main())
