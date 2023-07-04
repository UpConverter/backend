from fastapi import APIRouter, Query, HTTPException
from src.connection.models import *
from src.connection.service import *

router = APIRouter()


@router.get("/configs", response_model=list[Configuration])
async def get_configs():
    configs = await read_configs()
    return configs


@router.get("/configs/{config_id}", response_model=Configuration)
async def get_config(config_id: int):
    config = await read_config(config_id)
    if config:
        return config
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.get("/configs/{config_id}/connections", response_model=ConnectionsTyped)
async def get_config_connections(config_id: int):
    config_cals = await read_config_connections(config_id, device_type_name="CAL")
    config_upconv = await read_config_connections(config_id, device_type_name="UPCONVERTER")
    if config_cals or config_upconv:
        return {
            "config_cals": config_cals,
            "config_upconv": config_upconv
        }
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.get("/configs/{config_id}/cals", response_model=list[Connections])
async def get_config_cals(config_id: int):
    config_cals = await read_config_connections(config_id, device_type_name="CAL")
    if config_cals:
        return config_cals
    else:
        raise HTTPException(status_code=404, detail="Config not found")


@router.get("/configs/{config_id}/upconverters", response_model=list[Connections])
async def get_config_upconv(config_id: int):
    config_upconv = await read_config_connections(config_id, device_type_name="UPCONVERTER")
    if config_upconv:
        return config_upconv
    else:
        raise HTTPException(status_code=404, detail="Config not found")
