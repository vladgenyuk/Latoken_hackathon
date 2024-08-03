import json

from config import BOT_URL


async def send_message(session, chat_id, text, reply_markup: dict = None):
    url = BOT_URL + f"/sendMessage"

    data = {
        'text': text,
        'chat_id': chat_id,
        'parse_mode': 'Markdown'
    }

    if reply_markup is not None:
        data.update({'reply_markup': json.dumps(reply_markup)})

    async with session.post(url, data=data) as resp:
        print(await resp.json())
        pass
