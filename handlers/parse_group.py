from aiogram import types
from loader import dp

from modules.parse_vk_group import VkParser

from loguru import logger


@dp.message_handler(commands='parse')
async def parser_metadata_group(message: types.Message):
    text = message.text
    parser_vk = VkParser()

    if len(text.split()) == 2:
        group = text.split()[1]
        text = f'Парсинг группы <b>{group}</b> закончился'
        logger.info(f'Начался парсинг группы {group}')
        await parser_vk.run_vk_parser(group)
        logger.info(f'Парсинг группы {group} закончен')
    else:
        text = 'Что-то пошло не так. Попробуй ещё раз.'

    await message.answer(text=text)
