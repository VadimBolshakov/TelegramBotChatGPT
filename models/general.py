from aiogram.dispatcher import Dispatcher
from aiogram.types import ContentType
from create import bot
from admin.logsetting import logger
from aiogram import types
from databases import database
import datetime
from admin import checking


# @dp.message_handler(content_types=ContentType.TEXT)
@checking.check_foul_language
async def askGPT(message: types.Message):
    # Get the user from message
    user_text = message.text
    user_first_name = message.from_user.first_name
    user_id = message.from_user.id
    logger.info(f"Enter in def askGPT user {user_first_name} (id:{user_id})")

    # Checking user registration
    try:
        if database.get_db_user(message.from_user.id) is None:
            await message.answer("Вы не зарегистрированы. Введите команду start")
            logger.warning(f"Fail the registration check user {user_first_name} (id:{user_id})")
            return
        logger.info(f"Passed the registration check user {user_first_name} (id:{user_id})")

    except Exception as e:
        logger.exception(f"Error DB reads: {str(e)} from {user_first_name} (id:{user_id}")
        await message.answer(f"Error DB reads: {str(e)} from {user_first_name} (id:{user_id}")
        return



    msg = await bot.send_message(message.chat.id, 'Минуточку....')

    # Query OpenAI
    # openai.api_key = GPT_API_KEY
    # num_tokens = 0
    # status = 0
    # try:
    #     logger.info(f"Query OpenAI from user {user_first_name} (id:{user_id})")
    #     response = openai.Completion.create(
    #         engine="text-davinci-003",
    #         prompt=user_text,
    #         max_tokens=550,
    #         temperature=0.2,
    #         top_p=1,
    #         n=1,
    #         stop=None
    #     )
    #     # Get the response from OpenAI and send it back to the user
    #     logger.info(f"Get the response successful for user {user_first_name} (id:{user_id})")
    #     status = 1
    #     num_tokens = response["usage"]["total_tokens"]
    #     await msg.delete()
    #     await bot.send_message(message.chat.id, response["choices"][0]["text"])
    #
    # # except openai.error as e:
    # #     await msg.delete()
    # #     await bot.send_message(message.chat.id, 'Простите, но я сейчас занят\U0001FAE3')
    # #     logger.error(f"Request failed: {str(e)} from {user_name} (id:{user_id}")
    #
    # except Exception as e:
    #     await msg.delete()
    #     await bot.send_message(message.chat.id, 'О-п-с, что-то пошло не так.\U0001FAE2')
    #     logger.exception(f"Unexpected error: {str(e)} from {user_first_name} (id:{user_id}")

    # DB records
    # try:
    #     database.add_db_request(user_id=message.from_user.id,
    #                             date=datetime.datetime.now(),
    #                             num_tokens=num_tokens,
    #                             status=status)
    #     logger.info(f"Create DB records in requests table successful for user {user_first_name} (id:{user_id})")
    #
    # except Exception as e:
    #     logger.exception(f"Error DB records: {str(e)} from {user_first_name} (id:{user_id}")


#@dp.message_handler()
async def not_text(message: types.Message):
    await message.answer("Я понимаю только текст")

def register_handlers_general(dp: Dispatcher):
    dp.register_message_handler(askGPT, content_types=ContentType.TEXT)
    dp.register_message_handler(not_text, content_types=ContentType.ANY)


if __name__ == '__main__':
    pass
