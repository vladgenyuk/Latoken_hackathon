import asyncio
import aiohttp

import handlers

from config import BOT_URL, USER_STATES, USER_DATA


async def get_updates(session, offset=None):
    url = BOT_URL + "/getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    async with session.get(url) as resp:
        return await resp.json()


async def processor(session: aiohttp.ClientSession, update: dict):
    if update.get('callback_query'):
        chat_id: int = update.get('callback_query').get('from').get('id')
        callback_func_code = update.get('callback_query').get('data').split('-')[0]

        # await callback_functions[callback_func_code](
        #     session=session,
        #     user_id=chat_id,
        #     callback_data=update.get('callback_query').get('data'),
        #     message_id=update.get('callback_query')['message']['message_id']
        # )
        return chat_id
    elif update.get('message'):

        if update.get('message').get('text') and update.get('message').get('chat').get('id'):
            chat_id: int = update["message"]["chat"]["id"]
            message: str = update["message"]["text"]
            if USER_STATES != {}:
                await conversation_functions[USER_STATES.get(chat_id)](
                    session=session,
                    chat_id=chat_id,
                    message_text=message
                )
                return update.get('message').get('from').get('id')
            if message in commands_functions.keys():
                await commands_functions[message](
                    session=session,
                    chat_id=chat_id,
                )
                return update.get('message').get('from').get('id')
            await handlers.text_handler(
                session=session,
                chat_id=chat_id,
                text=message
            )
            return update.get('message').get('from').get('id')

commands_functions = {
    '/help': handlers.help_handler,
    '/start': handlers.start_handler,
    '/about_hackathon': handlers.about_hackathon_handler,
    '/about_culture_deck': handlers.about_culture_deck_handler,
    '/about_latoken': handlers.about_latoken_handler,

    '/rag_culture_test': handlers.rag_question1_handler,
    '/general_test': handlers.gt_question1_handler,
}

# callback_functions = {
#     'hi': hi_handler,
# }

conversation_functions = {}
conversation_functions.update(handlers.rag_conversation_functions)
conversation_functions.update(handlers.gt_conversation_functions)


async def main():
    last_update_id = None

    async with aiohttp.ClientSession() as session:
        while True:
            updates = await get_updates(session, last_update_id)
            print(updates)
            if 'result' in updates and len(updates['result']) > 0:
                for update in updates["result"]:
                    user_id = await processor(session=session, update=update)
                    last_update_id = update['update_id'] + 1


if __name__ == '__main__':
    asyncio.run(main())
