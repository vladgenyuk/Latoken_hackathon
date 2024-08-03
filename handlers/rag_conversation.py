import aiohttp

from utils.request_gpt import request_gpt
from utils.send_message import send_message

from config import USER_DATA, USER_STATES, TESTS_INIT_MESSAGE

QUESTIONS = {
    '1': '1: Как вы относитесь к вашим потенциальным пользователям? ',
    '2': '2: Ищите ли вы оправдания или причины для того, чтобы не работать? ',
    '3': '3: Опиши, насколько ты прозрачен в своей работе и в коммуникации с коллегами, оцени уровень своей ответственности. ',
    '4': '4: Открыт ли ты к обратной связи и критике? ',
    '5': '5: Как ты можешь использовать обратную связь или критику? '
}

CORRECT_ANSWERS = '''
    1)Клиентоориентированность:
            Приоритет клиентов над личным эго.
            Избегать воспитания обид или эгоистичных интересов.
        2)Выполнение вместо оправданий:
            "Покажи или умри" подчеркивает важность достижения результатов и недопустимость оправданий.
            Удалять людей, которые не соответствуют этому фокусу.
        3)Прозрачность и ответственность:
            Обеспечивать прозрачность и ответственность как в своей работе, так и в работе команды.
            Решать проблемы, связанные с халявщиками, и устранять блокеры совместными усилиями.
        4)Открытая обратная связь:
            Давать честную обратную связь для улучшения производительности.
            Избегать разговоров за спиной.
        5)Рост на основе обратной связи:
            Использовать обратную связь конструктивно для роста и улучшения.
            Сохранять настойчивость и стойкость, никогда не сдаваться и не бросать начатое.
'''


async def rag_question1_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    await send_message(session=session, chat_id=chat_id, text=TESTS_INIT_MESSAGE)
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('1')}🤔")
    USER_STATES[chat_id] = 'RAG_AWAITING_ANSWER_1'


async def rag_question2_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    answer = kwargs.get('message_text').strip().lower()
    USER_DATA[chat_id] = {'1': answer}
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('2')}🤔")
    USER_STATES[chat_id] = 'RAG_AWAITING_ANSWER_2'


async def rag_question3_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    answer = kwargs.get('message_text').strip().lower()
    USER_DATA[chat_id]['2'] = answer
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('3')}")
    USER_STATES[chat_id] = 'RAG_AWAITING_ANSWER_3'


async def rag_question4_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    answer = kwargs.get('message_text').strip().lower()
    USER_DATA[chat_id]['3'] = answer
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('4')}🤔")
    USER_STATES[chat_id] = 'RAG_AWAITING_ANSWER_4'


async def rag_question5_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    answer = kwargs.get('message_text').strip().lower()
    USER_DATA[chat_id]['4'] = answer
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('5')}🤔")
    USER_STATES[chat_id] = 'RAG_AWAITING_ANSWER_5'


async def rag_final_response_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    answer = kwargs.get('message_text').strip().lower()
    USER_DATA[chat_id]['5'] = answer
    await send_message(session=session, chat_id=chat_id, text="Спасибо, что ответили на все вопросы!")

    prompt = f'''
        У меня есть 5 вопросов и ответы в виде json, соотнеси вопросы и ответы и скажи на сколько % из 100 человек подходит компании Латокен.
        
        Вопросы:
            {QUESTIONS}
        
        Ответы пользователя:
            {USER_DATA.get(chat_id)}
        
        Правильные ответы:
            {CORRECT_ANSWERS}
        
        Оценивай самостоятельно.
        В своем ответе укажи процент того, на сколько человек подходит компании латокен, учитывай его старания при прохождении теста, если он отправляет просто да или хорошо, то давай ему меньше очков.
        В ответе отправь просто предложение "Вы подходите нам на n процентов", не шли пользователю вычисление оценки.
        Также отошли ему небольшое сообщение о нашей культуре (смотри правильные ответы).
        Если процент меньше 70, отправь сообщение "Вы подходите нам на n процентов, увы, этого не достаточно 😔" 
    '''
    resp = await request_gpt(session=session, text=prompt)

    await send_message(
        session=session,
        chat_id=chat_id,
        text=resp,
    )

    USER_STATES.pop(chat_id, None)
    USER_DATA.pop(chat_id, None)


rag_conversation_functions = {
    'RAG_AWAITING_ANSWER_1': rag_question2_handler,
    'RAG_AWAITING_ANSWER_2': rag_question3_handler,
    'RAG_AWAITING_ANSWER_3': rag_question4_handler,
    'RAG_AWAITING_ANSWER_4': rag_question5_handler,
    'RAG_AWAITING_ANSWER_5': rag_final_response_handler,
}
