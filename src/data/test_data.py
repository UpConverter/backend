import asyncio
from src.data.fill_database import fill_database

# SA
data = {
    # SA
    "SA" : {
        "Device": [
            {"name": "SA", "serial_number": 1000001, "type_id": 1},
        ],
        "Configuration": [
            {"name": "Конфигурация 1"},
            {"name": "Конфигурация 2"},
            {"name": "Конфигурация 3"},
            {"name": "Конфигурация 4"},
            {"name": "Конфигурация 5"},
        ],
        "Connection": [
            {"configuration_id": 1, "device_id": 2, "connected_to_device_id": 1,
             "connected_to_device_channel_id": 6},

            {"configuration_id": 1, "device_id": 5, "connected_to_device_id": 2,
             "connected_to_device_channel_id": 1},
            {"configuration_id": 1, "device_id": 6, "connected_to_device_id": 2,
             "connected_to_device_channel_id": 3},
            {"configuration_id": 1, "device_id": 7, "connected_to_device_id": 2,
             "connected_to_device_channel_id": 4},
            {"configuration_id": 1, "device_id": 8, "connected_to_device_id": 2,
             "connected_to_device_channel_id": 5},

            {"configuration_id": 1, "device_id": 9, "connected_to_device_id": 3,
             "connected_to_device_channel_id": 1},
            {"configuration_id": 1, "device_id": 10, "connected_to_device_id": 3,
             "connected_to_device_channel_id": 2},
            {"configuration_id": 1, "device_id": 11, "connected_to_device_id": 3,
             "connected_to_device_channel_id": 3},
            {"configuration_id": 1, "device_id": 12, "connected_to_device_id": 3,
             "connected_to_device_channel_id": 4},
        ],
    },
    # CAl
    "CAL" : {
        "Device": [

            {"name": "Cal 1", "serial_number": 1000002, "type_id": 2,
             "model_id": 1, "state_id": 0},
            {"name": "Cal 2", "serial_number": 1000003, "type_id": 2,
             "model_id": 2, "state_id": 0},
            {"name": "Cal 3", "serial_number": 1000004, "type_id": 2,
             "model_id": 2, "state_id": 0},
        ],
    },
    #UPCONVERTER
    "UPCONVERTER" : {
        "Device": [
            # UPCONVERTERS
            {"name": "UPCONVERTER 1", "serial_number": 1000006, "type_id": 3, "model_id": 1,
             "state_id": 2, "additional_state_id": 1},
            {"name": "UPCONVERTER 2", "serial_number": 1000007, "type_id": 3, "model_id": 1,
             "state_id": 1, "additional_state_id": 2},
            {"name": "UPCONVERTER 3", "serial_number": 1000008, "type_id": 3, "model_id": 2,
             "state_id": 3, "additional_state_id": 1},
            {"name": "UPCONVERTER 4", "serial_number": 1000009, "type_id": 3, "model_id": 2,
             "state_id": 3, "additional_state_id": 1},
            {"name": "UPCONVERTER 5", "serial_number": 1000010, "type_id": 3, "model_id": 1,
             "state_id": 1, "additional_state_id": 2},
            {"name": "UPCONVERTER 6", "serial_number": 1000011, "type_id": 3, "model_id": 2,
             "state_id": 3, "additional_state_id": 2},
            {"name": "UPCONVERTER 7", "serial_number": 1000012, "type_id": 3, "model_id": 2,
             "state_id": 2, "additional_state_id": 2},
            {"name": "UPCONVERTER 8", "serial_number": 1000013, "type_id": 3, "model_id": 2,
             "state_id": 1, "additional_state_id": 1},
        ],
    }
}

# Вызов функции заполнения базы данных при необходимости
async def main():
    for key in data:
        await fill_database(data[key])

# Запуск сопрограммы
asyncio.run(main())
