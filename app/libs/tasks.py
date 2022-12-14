import asyncio

import aioschedule
from loguru import logger

from app.database.models import Group
from app.libs.vk_parser import VkParser
from app.loader import session


async def autoparse_vk():
    """
    Собираю данные с таблицы groups, где в колонке autoparse значение True
    На выходе получается список с группами, который нужно "спарсить"
    Далее вызываю объект класса VkParser и вызываю функцию run_vk_parser()
    В неё передаю параметр: группы
    """
    vk_parser = VkParser()
    groups_autoparse = session.query(Group.screen_name).filter(Group.autoparse == "true").all()

    for screen_name in groups_autoparse:
        logger.info(f"Автопарсинг группы {screen_name[0]} начался")
        await vk_parser.run_vk_parser(screen_name[0])
        logger.info(f"Автопарсинг группы {screen_name[0]} закончен")


async def schedule():
    aioschedule.every().day.at("8:00").do(autoparse_vk)
    aioschedule.every().day.at("20:00").do(autoparse_vk)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
