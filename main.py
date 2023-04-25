# @Vadim_AI_Bot

from create import dp, bot
from logsetting import logger
from models import start, general
from aiogram.utils import executor
from databases import database


async def on_startup(_):
    logger.info('Bot in online')
    print('Bot in online')
    database.start_db()
    print('Db created')
    logger.info('DB created')


start.register_handlers_start(dp)

general.register_handlers_general(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
