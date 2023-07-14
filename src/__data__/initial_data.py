import asyncio

from src.__data__.fill_database import fill_database

data = {
    "DeviceType": [{"name": "SA"}, {"name": "CAL"}, {"name": "UPCONVERTER"}],
    "DeviceModel": [
        {"name": "COAXIAL"},
        {"name": "SMDvA"},
        {"name": "SMD"},
    ],
    "DeviceState": [{"name": "CRYO"}, {"name": "CAL"}, {"name": "TERMINATE"}],
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
        {"name": "CH7"},
    ],
    "Speed": [
        {"value": 57600},
        {"value": 256000},
        {"value": 115200},
        {"value": 921600},
    ],
    "Port": [
        {"name": "COM1"},
        {"name": "COM2"},
        {"name": "COM3"},
        {"name": "COM4"},
    ],
    "Device": [
        {"name": "SA", "serial_number": "000000", "type_id": 1},
    ],
}

# Вызов функции заполнения базы данных при необходимости


async def main():
    await fill_database(data)


# Запуск сопрограммы
asyncio.run(main())
