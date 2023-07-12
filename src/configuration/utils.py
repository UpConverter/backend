import re

from sqlalchemy import select

from src import schemas
from src.database import database


async def gen_unique_config_name() -> str:
    base_name = "New config"

    # Получаем все имена конфигураций, начинающиеся с "New config" из базы данных
    select_query = select(schemas.Configuration.name).where(
        schemas.Configuration.name.like(f"{base_name}%")
    )
    matching_names = await database.fetch_all(select_query)

    suffixes = []
    names = [row[0] for row in matching_names]
    for name in names:
        match = re.search(rf"{base_name}\s(\d+)", name)
        if match:
            suffixes.append(int(match.group(1)))

    # Выбираем максимальный суффикс и формируем новое имя конфигурации
    if suffixes:
        max_suffix = max(suffixes)
        config_name = f"{base_name} {max_suffix + 1}"
    else:
        config_name = f"{base_name} 1"

    return config_name
