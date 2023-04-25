# Authentication new user by password
# Used FSM
from aiogram import Dispatcher, types
from create import bot, password
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from databases import database


class RegisterFSM(StatesGroup):
    password = State()


# @dp.message_handler(commands=['start', 'help'], state=None)
async def command_start_help(message: types.Message):
    if database.get_db_user(message.from_user.id) is None:
        await message.answer("Enter password")
        await RegisterFSM.password.set()
    else:
        await message.answer(f'Здравствуйте {message.from_user.full_name}.\n'
                             f'Этот бот отвечает на вопросы с помощью GPT-3.\n'
                             f'Задайте свой вопрос ниже \U0001F604')


# @dp.message_handler(state=RegisterFSM.password)
async def input_password(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['password'] = message.text.split()
    if data['password'][0] == password:

        database.add_db_user(user_id=message.from_user.id,
                             first_name=message.from_user.first_name,
                             full_name=message.from_user.full_name,
                             user_name=message.from_user.username,
                             date_registration=message.date)
        await bot.send_message(message.chat.id, f'Здравствуйте {message.from_user.full_name}.\n'
                                                f'Этот бот отвечает на вопросы с помощью GPT-3.\n'
                                                f'Задайте свой вопрос ниже\U0001F604')
        await state.finish()
    else:
        await message.answer('The password is incorrect')
        await message.answer("Enter password")


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(command_start_help, commands=['start', 'help'], state=None)
    dp.register_message_handler(input_password, state=RegisterFSM.password)


if __name__ == '__main__':
    pass
