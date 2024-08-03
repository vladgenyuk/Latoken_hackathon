import aiohttp

from utils.send_message import send_message
from utils.request_gpt import request_gpt


async def start_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    prompt = '''
        Расскажи про моего бота
        start 
        about_hackathon 
        about_culture_deck 
        about_latoken 
        rag_culture_test
        general_test
        
        Не используй запрещенных символов в телеграмм, чтобы не возникло ошибки "Bad Request: can't parse entities: Can't find end of the entity starting at byte offset 1758"
        Сделай красивое оформление, не используй текст от себя
        '''
    resp = await request_gpt(session=session, text=prompt)
    await send_message(session=session, chat_id=chat_id, text=resp)
