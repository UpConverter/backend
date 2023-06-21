from .fill_database import fill_database

data = {
    "DeviceType": [
        {"id": 0, "name": "SA"},
        {"id": 1, "name": "CAL"},
        {"id": 2, "name": "UPCONVERTER"}
    ],
    "DeviceModel": [
        {"id": 0, "name": "COAXIAL"},
        {"id": 1, "name": "SOLID STATE"}
    ],
    "DeviceState": [
        {"id": 0, "name": "CRYO"},
        {"id": 1, "name": "CAL"},
        {"id": 2, "name": "TERMINATE"}
    ],
    "DeviceAdditionalState": [
        {"id": 0, "name": "LO_FULL"},
        {"id": 1, "name": "LO_SPLIT"},
    ],
    "Channel": [
        {"id": 0, "name": "CH1"},
        {"id": 1, "name": "CH2"},
        {"id": 2, "name": "CH3"},
        {"id": 3, "name": "CH4"},
        {"id": 4, "name": "CH5"},
        {"id": 5, "name": "CH6"},
    ],
    "Speed": [
        {"id": 0, "value": 57600},
        {"id": 1, "value": 256000},
        {"id": 2, "value": 115200},
        {"id": 3, "value": 921600}
    ],
    "Port": [
        {"id": 0, "name": "COM1"},
        {"id": 1, "name": "COM2"},
        {"id": 2, "name": "COM3"},
        {"id": 3, "name": "COM4"},
    ],
}

# Вызов функции заполнения базы данных при необходимости
fill_database(data)
