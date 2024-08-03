from config import API_KEY


async def request_gpt(session, text: str):

    url = 'https://api.openai.com/v1/chat/completions'

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }

    data = {
        'model': 'gpt-4o',
        'messages': [
            {'role': 'user', 'content': text}
        ],
    }

    async with session.post(url, json=data, headers=headers) as resp:
        response_data = await resp.json()
        if response_data.get('choices'):
            return response_data.get('choices')[0].get('message').get('content')
        # print(response_data)
        return 'Error'
