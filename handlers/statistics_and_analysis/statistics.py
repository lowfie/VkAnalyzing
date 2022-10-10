from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from loader import dp

from datetime import datetime, timedelta

from database import Analytics
from database.models import Group, Post

from .statistics_state import StatisticsFormState


@dp.message_handler(commands='stats', state=None)
async def cm_stats(message: types.Message):
    await StatisticsFormState.name.set()
    await message.reply('Введите название группы из ссылки')


@dp.message_handler(state=StatisticsFormState.name, content_types=['text'])
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.reply('Введите период подсчёта статистики (в днях)')
    await StatisticsFormState.next()


@dp.message_handler(state=StatisticsFormState.days, content_types=['text'])
async def load_period(message: types.Message, state: FSMContext):
    analysis = Analytics(group=Group, post=Post)
    async with state.proxy() as data:
        data['date'] = datetime.now() - timedelta(days=int(message.text))

    statistics = analysis.get_statistic(data)
    most_positive_post = analysis.get_tops_stats(data, Post.positive_comments)
    most_negative_post = analysis.get_tops_stats(data, Post.negative_comments)
    most_popular_post = analysis.get_tops_stats(data, Post.views)

    if statistics:
        text = f"""
За {(datetime.now() - data["date"]).days} дней было собрано {statistics["count_post"]} постов
Посты с фото/видео: {statistics["posts_with_photo"]}
Лайки: {statistics["likes"]}
Комментарии: {statistics["comments"]}
Репосты: {statistics["reposts"]}
Всего просмотров: {statistics["views"]}\n\n
{hlink("Самый популярный пост", most_popular_post)}
{hlink("Самый позитивный пост", most_positive_post)}
{hlink("Самый негативный пост", most_negative_post)}
"""
        parse_mode = 'html'
    else:
        text = f"""
К сожалению группы {data["name"]} нету в базе
Вы можете её добавить написать /group <name>
"""
        parse_mode = None

    await dp.bot.send_message(
        chat_id=message.chat.id,
        text=text,
        disable_web_page_preview=True,
        parse_mode=parse_mode
    )

    await state.finish()