from fastapi import status

from src.exceptions import BadRequest, DetailedHTTPException
from src.visa.constants import ErrorCode


class VisaIOError(DetailedHTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Visa IO Error"


class ConnectError(BadRequest):
    DETAIL = ErrorCode.DEVICE_PORT_NOT_EXIST


class SANotExistError(BadRequest):
    DETAIL = ErrorCode.SA_NOT_EXIST_ERROR


class ManySADevicesError(BadRequest):
    DETAIL = ErrorCode.MANY_SA_DEVICES_ERROR


class ConnectedToSAError(BadRequest):
    DETAIL = ErrorCode.CONNECTED_TO_SA_ERROR


class InvalidConncetionError(BadRequest):
    DETAIL = ErrorCode.INVALID_CONNECTION_ERROR


class StateChangeError(BadRequest):
    DETAIL = ErrorCode.STATE_CHANGE_ERROR


class UnknownError(DetailedHTTPException):
    DETAIL = ErrorCode.UNKNOWN_ERROR
