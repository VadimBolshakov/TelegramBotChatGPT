# @Vadim_AI_Bot

from create import dp
from admin.logsetting import logger
from models import start, general, sendadmin
from aiogram.utils import executor
from databases import database


async def on_startup(_):
    logger.info('Bot in online')
    database.start_db()
    logger.info('DB created')


start.register_handlers_start(dp)
sendadmin.register_handlers_sendadmin(dp)
general.register_handlers_general(dp)


async def on_shutdown():
    await dp.storage.close()
    await dp.storage.wait_closed()


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
