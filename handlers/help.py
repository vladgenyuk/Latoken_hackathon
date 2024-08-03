import aiohttp

from utils.send_message import send_message


async def help_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    await send_message(session=session, chat_id=chat_id, text=f'Help')
