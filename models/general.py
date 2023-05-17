import openai
from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ContentType
from admin import checking
from admin.logsetting import logger
from create import bot
from databases import database
from create import GPT_API_KEY
from datetime import datetime


# @dp.message_handler(content_types=ContentType.TEXT)
@checking.check_registration
@checking.check_foul_language
async def askGPT(message: types.Message):
    # Get the user from message
    user_text = message.text
    user_first_name = message.from_user.first_name
    user_id = message.from_user.id
    logger.info(f'Enter in def askGPT user {user_first_name} (id:{user_id})')

    msg = await bot.send_message(message.chat.id, 'Минуточку....')

    # Query OpenAI
    openai.api_key = GPT_API_KEY
    num_tokens = 0
    status = 0
    try:
        logger.info(f'Query OpenAI from user {user_first_name} (id:{user_id})')
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=user_text,
            max_tokens=550,
            temperature=0.2,
            top_p=1,
            n=1,
            stop=None
        )
        # Get the response from OpenAI and send it back to the user
        logger.info(f'Get the response successful for user {user_first_name} (id:{user_id})')
        status = 1
        num_tokens = response['usage']['total_tokens']
        await msg.delete()
        await bot.send_message(message.chat.id, response['choices'][0]['text'])
        logger.info(f'Send message successful for user {user_first_name} (id:{user_id})')

    except openai.error.InvalidRequestError as e:
        await msg.delete()
        await bot.send_message(message.chat.id, 'О-п-с, что-то пошло не так.\U0001FAE2')
        logger.exception(f'Openai error: {str(e)} from {user_first_name} (id:{user_id}')

    except openai.error.AuthenticationError as e:
        await msg.delete()
        await bot.send_message(message.chat.id, 'О-п-с, что-то пошло не так.\U0001FAE2')
        logger.exception(f'Openai error: {str(e)} from {user_first_name} (id:{user_id}')

    except openai.error.APIConnectionError as e:
        await msg.delete()
        await bot.send_message(message.chat.id, 'О-п-с, что-то пошло не так.\U0001FAE2')
        logger.exception(f'Openai error: {str(e)} from {user_first_name} (id:{user_id}')

    except openai.error.OpenAIError as e:
        await msg.delete()
        await bot.send_message(message.chat.id, 'О-п-с, что-то пошло не так.\U0001FAE2')
        logger.exception(f'Openai error: {str(e)} from {user_first_name} (id:{user_id}')

    except TimeoutError as e:
        await msg.delete()
        await bot.send_message(message.chat.id, 'О-п-с, что-то пошло не так.\U0001FAE2')
        logger.exception(f'TimeoutError error: {str(e)} from {user_first_name} (id:{user_id}')

    except Exception as e:
        await msg.delete()
        await bot.send_message(message.chat.id, 'О-п-с, что-то пошло не так.\U0001FAE2')
        logger.exception(f'Unexpected error: {str(e)} from {user_first_name} (id:{user_id}')

    # DB records
    try:
        database.add_request(user_id=message.from_user.id,
                             date=datetime.now(),
                             num_tokens=num_tokens,
                             status=status)
        logger.info(f'Create DB records in requests table successful for user {user_first_name} (id:{user_id})')

    except Exception as e:
        logger.exception(f'Error DB records: {str(e)} from {user_first_name} (id:{user_id}')


# @dp.message_handler()
@checking.check_registration
async def not_text(message: types.Message):
    await message.answer('Я понимаю только текст')
    # await message.answer('I understand only text')
    await message.delete()


def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(askGPT, content_types=ContentType.TEXT)
    dp.register_message_handler(not_text, content_types=ContentType.ANY)


if __name__ == '__main__':
    pass
