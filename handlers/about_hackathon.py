import aiohttp

from utils.send_message import send_message
from utils.request_gpt import request_gpt


async def about_hackathon_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    prompt = '''
        Сделай руководство по разработке AI бота для Telegram, который будет помогать кандидатам узнать детали работы в Латокен и процесса интервью. Учитывай следующие уровни сложности:

        1) No code: Бот отвечает на вопросы о Латокен и Хакатонах.
        2) Code + О Латокен и Хакатонах: Бот использует код на любом языке для предоставления информации.
        3) Code + О Латокен и Хакатонах + RAG Culture Deck: Бот отвечает на вопросы и включает элементы Culture Deck.
        4) Code + О Латокен и Хакатонах + RAG Culture Deck + Test: Бот задает вопросы для тестирования кандидатов.
        5) 4+ Tuning
        
        Кроме того, добавь информацию о том, как провести демонстрацию бота и какие материалы могут быть полезны для работы, добавь ссылки на: документацию АПИ телеграмм, ссылка на хакатон (https://latoken.me/ai-bot-hackathon-task-190), ссылка на страницеу о Латокен (https://coda.io/@latoken/latoken-talent/latoken-161), ссылка на Culture Deck (https://coda.io/@latoken/latoken-talent/culture-139).
        (
            ДЕМО В СБ 18:00 МСК (Скиньте вашего бота в 17:15 https://discord.gg/vR9ak7CHdV. Мы сначала проверяем, что ваш бот работает, а потом приглашаем на сцену)
        )

        Также упомяни о возможности создания простого работающего бота и альтернативных задаче, создание веб-апп кликера.
        Умести ответ в небольшом тексте - 200 слов.
        Сделай красивое форматирование в телеграмм, не используя хештеги, не вставляй отрывки кода, используй эмоджи.
    '''
    resp = await request_gpt(session=session, text=prompt)

    await send_message(
        session=session,
        chat_id=chat_id,
        text=resp,
    )
