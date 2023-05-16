from aiogram import types
import string
import json
from admin.logsetting import logger


# Checking the foul language text into message
def check_foul_language(fn):
    async def wrapper(message: types.Message):
        user_text = message.text
        user_first_name = message.from_user.first_name
        user_id = message.from_user.id
        if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in user_text.split(' ')} \
                .intersection(set(json.load(open('foul.json')))):
            await message.reply('Это не хорошо, говорить такие слова')
            # await message.reply('foul language is prohibited')
            if message: await message.delete()
            logger.warning(f"Fail the foul language check user {user_first_name} (id:{user_id})")
            return
        logger.info(f"Passed the foul language check user {user_first_name} (id:{user_id})")
        await fn(message)

    return wrapper
