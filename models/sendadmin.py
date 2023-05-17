from create import bot
from admin.logsetting import logger
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
import os
from dotenv import load_dotenv, find_dotenv
from admin import smtp
from databases import database
from datetime import datetime

load_dotenv(find_dotenv())
LOG_FILE = os.getenv('LOG_FILE')


class AdminFSM(StatesGroup):
    broadcast = State()


# @dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    """Send message to admin about using commands."""
    await message.answer('Admin panel suggest using next commands:\n'
                         '/getlog - send log file to telegram\n'
                         '/getemail - send log file to email\n'
                         '/getusers - send id and users of this chat to admin\n'
                         '/getrequests - send number of requests to admin\n'
                         '/sendall - send message to all users\n')


# @dp.message_handler(commands=['getlog'])
async def send_log(message: types.Message):
    """Send log file to admin in telegram."""
    try:
        with open(LOG_FILE, 'rb') as file:
            await message.answer_document(file)
    except Exception as e:
        logger.exception(f'Error: {str(e)}')
        await message.answer('Error send log file')


# @dp.message_handler(commands=['getemail'])
async def send_email_lod(message: types.Message):
    """Send log file to admin in email."""
    subject = f'Log file by {datetime.now()}'[:19]
    # subject = f'Log file by {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    smtp.send_email(subject=subject, file=LOG_FILE, attach_file=True)
    await message.answer('Log file send to email')


# @dp.message_handler(commands=['getusers'])
async def send_users(message: types.Message):
    """Send id and users of this chat to admin."""
    users = database.get_all_users()
    for user in users:
        await message.answer(user)


# @dp.message_handler(commands=['getrequests'])
async def send_requests(message: types.Message):
    """Send number of requests to admin."""
    requests = database.get_requests_count()
    await message.answer(f'Number of  requests is {requests}')


# @dp.message_handler(commands=['sendall'], state=None)
async def send_all(message: types.Message):
    """Send message to all users."""
    await message.answer('Enter message (enter "/cancel" to cancel)')
    await AdminFSM.broadcast.set()


# @dp.message_handler(state=AdminFSM.broadcast)
async def send_all_message(message: types.Message, state: FSMContext):
    """Send message to all users."""
    async with state.proxy() as data:
        data['broadcast'] = message.text
    if data['broadcast'] == '/cancel':
        await message.answer('Cancel')
        return
    users = database.get_all_users()
    for user in users:
        try:
            await bot.send_message(user[1], data['broadcast'])
        except Exception as e:
            logger.exception(f'Error send message to {user} {e}')
            await message.answer(f'Error send message to {user} {e}')
    await message.answer('Message send')
    await state.finish()


def register_handlers_sendadmin(dp: Dispatcher):
    dp.register_message_handler(admin, commands=['admin'])
    dp.register_message_handler(send_log, commands=['getlog'])
    dp.register_message_handler(send_email_lod, commands=['getemail'])
    dp.register_message_handler(send_users, commands=['getusers'])
    dp.register_message_handler(send_requests, commands=['getrequests'])
    dp.register_message_handler(send_all, commands=['sendall'], state=None)
    dp.register_message_handler(send_all_message, state=AdminFSM.broadcast)


if __name__ == '__main__':
    pass
