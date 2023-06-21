from .fill_database import fill_database

data = {
    "Device": [
        # SA
        {"id": 0, "serial_number": 1000001, "type_id": 0},

        # CALS
        {"id": 1, "serial_number": 1000002, "type_id": 1,
         "model_id": 0},
        {"id": 2, "serial_number": 1000003, "type_id": 1,
         "model_id": 1},
        {"id": 3, "serial_number": 1000004, "type_id": 1,
         "model_id": 1},

        # UPCONVERTERS
        {"id": 5, "serial_number": 1000006, "type_id": 2,
         "model_id": 0, "state_id": 1, "additional_state_id": 0},
        {"id": 6, "serial_number": 1000007, "type_id": 2,
         "model_id": 0, "state_id": 0, "additional_state_id": 1},
        {"id": 7, "serial_number": 1000008, "type_id": 2,
         "model_id": 1, "state_id": 2, "additional_state_id": 0},
        {"id": 8, "serial_number": 1000009, "type_id": 2,
         "model_id": 1, "state_id": 2, "additional_state_id": 0},
        {"id": 9, "serial_number": 1000010, "type_id": 2,
         "model_id": 0, "state_id": 0, "additional_state_id": 1},
        {"id": 10, "serial_number": 1000011, "type_id": 2,
         "model_id": 1, "state_id": 2, "additional_state_id": 1},
        {"id": 11, "serial_number": 1000012, "type_id": 2,
         "model_id": 1, "state_id": 1, "additional_state_id": 1},
        {"serial_number": 1000013, "type_id": 2,
         "model_id": 1, "state_id": 0, "additional_state_id": 0},
    ],
    "Configuration": [
        {"name": "Конфигурация 1", "speed_id": 0, "port_id": 0},
        {"name": "Конфигурация 2", "speed_id": 1, "port_id": 1},
        {"name": "Конфигурация 3", "speed_id": 1, "port_id": 1},
        {"name": "Конфигурация 4", "speed_id": 1, "port_id": 2},
        {"name": "Конфигурация 5", "speed_id": 1, "port_id": 3},
    ],
    "Connection": [
        {"configuration_id": 0, "device_id": 2, "connected_to_device_id": 1,
            "connected_to_device_channel_id": 5},

        {"configuration_id": 0, "device_id": 5, "connected_to_device_id": 1,
            "connected_to_device_channel_id": 0},
        {"configuration_id": 0, "device_id": 5, "connected_to_device_id": 1,
            "connected_to_device_channel_id": 1},
        {"configuration_id": 0, "device_id": 6, "connected_to_device_id": 1,
            "connected_to_device_channel_id": 2},
        {"configuration_id": 0, "device_id": 7, "connected_to_device_id": 1,
            "connected_to_device_channel_id": 3},
        {"configuration_id": 0, "device_id": 8, "connected_to_device_id": 1,
            "connected_to_device_channel_id": 4},

        {"configuration_id": 0, "device_id": 9, "connected_to_device_id": 2,
            "connected_to_device_channel_id": 0},
        {"configuration_id": 0, "device_id": 10, "connected_to_device_id": 2,
            "connected_to_device_channel_id": 1},
        {"configuration_id": 0, "device_id": 11, "connected_to_device_id": 2,
            "connected_to_device_channel_id": 2},
        {"configuration_id": 0, "device_id": 12, "connected_to_device_id": 2,
            "connected_to_device_channel_id": 3},
    ],
}

# Вызов функции заполнения базы данных при необходимости
fill_database(data)
