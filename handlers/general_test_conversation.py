import aiohttp

from utils.request_gpt import request_gpt
from utils.send_message import send_message

from config import USER_DATA, USER_STATES, TESTS_INIT_MESSAGE

QUESTIONS = {
    '1': '1: Какое место в мире занимает Latoken по количеству активов? ',
    '2': '2: Какие перспективы даёт Latoken в плане карьерного роста своим сотрудникам (можешь вспомнить технологии)? ',
    '3': '3: Какое место в списке Forbes занимает Latoken? ',
    '4': '4: Какое самое главное культурное правило в Latoken? ',
    '5': '5: Какая самая успешная компания в СНГ в WEB3?) ',

}

CORRECT_ANSWERS = '''
1) 1 - #1 по числу активов для трейдинга 3,000+ (Бинанс 400+)
2) Быстрый рост через решение нетривиальных задач
Передовые технологии AIxWEB3
Глобальный рынок, клиенты в 170+ странах 
Самая успешная компания из СНГ в WEB3
Входит в Top 30 Forbes компаний для удаленной работы
3) 30 - Входит в Top 30 Forbes компаний для удаленной работы
4) КУЛЬТУРА 
    ПОЛНЫЙ КОММИТМЕНТ РАСТИ, ЧТОБЫ БЫТЬ ПОЛЕЗНЕЕ,
    "БАЛАНС" И "СЧАСТЬЕ" НЕ ДЛЯ ЧЕМПИОНОВ
5) Latoken
'''


async def gt_question1_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    await send_message(session=session, chat_id=chat_id, text=TESTS_INIT_MESSAGE)
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('1')}🤔")
    USER_STATES[chat_id] = 'GT_AWAITING_ANSWER_1'


async def gt_question2_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    answer = kwargs.get('message_text').strip().lower()
    USER_DATA[chat_id] = {'1': answer}
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('2')}🤔")
    USER_STATES[chat_id] = 'GT_AWAITING_ANSWER_2'


async def gt_question3_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    answer = kwargs.get('message_text').strip().lower()
    USER_DATA[chat_id]['2'] = answer
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('3')}🤔")
    USER_STATES[chat_id] = 'GT_AWAITING_ANSWER_3'


async def gt_question4_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    answer = kwargs.get('message_text').strip().lower()
    USER_DATA[chat_id]['3'] = answer
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('4')}🤔")
    USER_STATES[chat_id] = 'GT_AWAITING_ANSWER_4'


async def gt_question5_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    answer = kwargs.get('message_text').strip().lower()
    USER_DATA[chat_id]['4'] = answer
    await send_message(session=session, chat_id=chat_id, text=f"Вопрос {QUESTIONS.get('5')}🤔")
    USER_STATES[chat_id] = 'GT_AWAITING_ANSWER_5'


async def gt_final_response_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
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
        В своем ответе укажи процент того, на сколько человек правильно ответил на вопросы, учитывай его старания при прохождении теста, если он отправляет просто да или хорошо, то давай ему меньше очков.
        В ответе отправь процент правильности выполнения теста, не шли пользователю вычисление оценки.
        Также отошли ему правильные ответы.
        Если процент меньше 70, отправь сообщение "Вы прошли тет на n %, пройдите тест заново с приобретёнными знаниями😊" 
    '''
    resp = await request_gpt(session=session, text=prompt)

    await send_message(
        session=session,
        chat_id=chat_id,
        text=resp,
    )

    USER_STATES.pop(chat_id, None)
    USER_DATA.pop(chat_id, None)


gt_conversation_functions = {
    'GT_AWAITING_ANSWER_1': gt_question2_handler,
    'GT_AWAITING_ANSWER_2': gt_question3_handler,
    'GT_AWAITING_ANSWER_3': gt_question4_handler,
    'GT_AWAITING_ANSWER_4': gt_question5_handler,
    'GT_AWAITING_ANSWER_5': gt_final_response_handler,
}
