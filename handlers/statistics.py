from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from loader import dp

from datetime import datetime, timedelta

from database import PostService
from database.models import Post


class FSMDate(StatesGroup):
    name = State()
    days = State()


@dp.message_handler(commands='stats',state=None)
async def cm_stats(message: types.Message):
    await FSMDate.name.set()
    await message.reply('Введите название группы из ссылки')


@dp.message_handler(state=FSMDate.name, content_types=['text'])
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = str(message.text)
    await message.reply('Введите период подсчёта статистики в днях')
    await FSMDate.next()


@dp.message_handler(state=FSMDate.days, content_types=['text'])
async def load_period(message: types.Message, state: FSMContext):
    post_service = PostService(Post)
    async with state.proxy() as data:
        data['date'] = datetime.now() - timedelta(days=int(message.text))

    statistics = post_service.get_statistic(data)

    if statistics:
        text = f'За {data["date"]} дней выложено {statistics["count_post"]} постов' \
                f'Посты с фото/видео: {statistics["posts_with_photo"]}\n' \
                f'Лайки: {statistics["likes"]}\n' \
                f'Всего просмотров: {statistics["likes"]}\n' \
                f'Комментарии: {statistics["comments"]}'
    else:
        text = f'К сожалению группы {data["name"]} нету в базе\n' \
               f'Вы можете её добавить написать /group <name>'

    await dp.bot.send_message(
        chat_id=message.chat.id,
        text=text
    )

    await state.finish()
