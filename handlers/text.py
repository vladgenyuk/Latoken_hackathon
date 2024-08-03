import aiohttp

from utils.send_message import send_message
from utils.request_gpt import request_gpt


async def text_handler(session: aiohttp.ClientSession, chat_id: int, text: str):
    resp = await request_gpt(session=session, text=text)
    await send_message(session=session, chat_id=chat_id, text=resp)
