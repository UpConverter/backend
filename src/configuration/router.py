from fastapi import APIRouter, HTTPException

from src.configuration.models import Configuration, ConfigurationCreate
from src.configuration.service import *
from src.configuration.utils import gen_unique_config_name
from src.connection.models import (
    Connection,
    ConnectionCreate,
    Connections,
    ConnectionsTyped,
)
from src.connection.service import create_connection
from src.device.models import DeviceRelated

router = APIRouter()


@router.get("/", response_model=list[Configuration])
async def get_configs():
    configs = await read_configs()
    return configs


@router.post("/new", response_model=Configuration)
async def create_new_config():
    config_name = await gen_unique_config_name()
    return await create_config(ConfigurationCreate(name=config_name))


@router.post("/", response_model=Configuration)
async def create_new_config(config: ConfigurationCreate):
    return await create_config(config)


@router.put("/{config_id}")
async def update_existing_config(config_id: int, configuration: ConfigurationCreate):
    config = await read_config(config_id)
    if config:
        await update_config(config_id, configuration)
        return {"message": "Configuration updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.delete("/{config_id}")
async def delete_existing_config(config_id: int):
    config = await read_config(config_id)
    if config:
        await delete_config(config_id)
        return {"message": f"Config deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.get("/{config_id}", response_model=Configuration)
async def get_config(config_id: int):
    config = await read_config(config_id)
    if config:
        return config
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.get("/{config_id}/connections", response_model=ConnectionsTyped)
async def get_config_connections(config_id: int):
    config = await read_config(config_id)
    if config:
        config_cals = await read_config_connections(config_id, device_type_name="CAL")
        config_upconv = await read_config_connections(
            config_id, device_type_name="UPCONVERTER"
        )
        return {"config_cals": config_cals, "config_upconv": config_upconv}
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.post("/{config_id}/connections", response_model=Connection)
async def create_new_connection(config_id: int, connection: ConnectionCreate):
    config = await read_config(config_id)
    if config:
        return await create_connection(config_id, connection)
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.put("/{config_id}/connections")
async def update_existing_config_connections(
    config_id: int, connections: ConnectionsTyped
):
    config = await read_config(config_id)
    if config:
        await update_config_connections(config_id, connections)
        return {"message": "Connections updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.get("/{config_id}/cals", response_model=list[Connections])
async def get_config_cals(config_id: int):
    config_cals = await read_config_connections(config_id, device_type_name="CAL")
    if config_cals:
        return config_cals
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.get("/{config_id}/upconverters", response_model=list[Connections])
async def get_config_upconv(config_id: int):
    config_upconv = await read_config_connections(
        config_id, device_type_name="UPCONVERTER"
    )
    if config_upconv:
        return config_upconv
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.get("/{config_id}/avaliable_devices", response_model=list[DeviceRelated])
async def get_config_avaliable_devices(config_id: int, type_name: str):
    config = await read_config(config_id)
    if config:
        devices = await read_config_avaliable_devices(config_id, type_name)
        return devices
    else:
        raise HTTPException(status_code=404, detail="Config not found")
