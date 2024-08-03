async def create_webapp_keyboard(text: str, url: str):
    keyboard = {
        "inline_keyboard": [
            [
                {
                    'text': text,
                    'web_app': {
                        "url": url
                    }
                },
            ]
        ],
        "one_time_keyboard": True
    }

    return keyboard
