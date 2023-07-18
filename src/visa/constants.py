class ErrorCode:
    DEVICE_PORT_NOT_EXIST = "Не удалось подключиться к устройству"
    UNKNOWN_ERROR = "Что-то пошло не так, попробуйте позже"
    SA_NOT_EXIST_ERROR = "Одно устройство должно быть подключено к SA"
    MANY_SA_DEVICES_ERROR = "Подключенный к SA модуль может быть только один"
    CONNECTED_TO_SA_ERROR = "Некоторые устройства не могут быть подключены к SA"
    INVALID_CONNECTION_ERROR = (
        "Соединение с устройством разорвано или передана неверная конфигурация"
    )
    STATE_CHANGE_ERROR = "Не удалось изменить состояние устройства"
    INVALID_DEVICE_NAME_ERROR = "Имя устройства не найдено в конфигурации"
    INVALID_DEVICE_MODEL_ERROR = "Модель устройства должна быть одной из существующих"
    CAL_MODEL_SMDVA_ERROR = "Модель калибровочного модуля не может быть SMDvA"
    VISA_ERROR = "Ошибка отправки команды в устройство"
