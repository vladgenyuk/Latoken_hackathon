import aiohttp

from utils.send_message import send_message
from utils.request_gpt import request_gpt


async def about_culture_deck_handler(session: aiohttp.ClientSession, chat_id: int, **kwargs):
    prompt = '''
        Расскажи о культуре Latoken, основываясь на следующем материале:
            Клиентоориентированность:
                Приоритет клиентов над личным эго.
                Избегать воспитания обид или эгоистичных интересов.
            Выполнение вместо оправданий:
                "Покажи или умри" подчеркивает важность достижения результатов и недопустимость оправданий.
                Удалять людей, которые не соответствуют этому фокусу.
            Прозрачность и ответственность:
                Обеспечивать прозрачность и ответственность как в своей работе, так и в работе команды.
                Решать проблемы, связанные с халявщиками, и устранять блокеры совместными усилиями.
            Открытая обратная связь:
                Давать честную обратную связь для улучшения производительности.
                Избегать разговоров за спиной.
            Рост на основе обратной связи:
                Использовать обратную связь конструктивно для роста и улучшения.
                Сохранять настойчивость и стойкость, никогда не сдаваться и не бросать начатое.
            Олимпийская свобода и ответственность:
                Стремиться к созданию культуры, сочетающей свободу и ответственность, движимой критически важными задачами.
            Культура как действия:
                Культура определяется действиями, а не только убеждениями.
                Она проявляется в том, как принимаются решения, особенно когда они не наблюдаются.
            Шокирующие правила:
                Внедрять четкие и строгие правила для обеспечения соответствия принципам компании.
                Пример: правило, требующее от сотрудников быть клиентами продукта, который они создают, для обеспечения истинного понимания и приверженности.
            Культура и инновации:
                Сильная, инновационная культура может стать отличительной чертой для новых компаний в борьбе с устоявшимися игроками.
                Культура развивается через экономическую конкуренцию и отбор, часто в условиях высокого риска.
            Эволюция культуры:
                Конкуренция между старыми и новыми культурами интенсивна, и быстрая эволюция культуры является ключом к выживанию.
                Эта "война" происходит на рынке, где продукт и цены являются оружием.
            Понимание механизмов:
                Интуиции недостаточно; важно понимать основные механизмы.
        
    Умести ответ в небольшом тексте - 200 слов.
    Сделай красивое форматирование в телеграмм, не используя хештеги, не вставляй отрывки кода, используй эмоджи.    
    '''
    resp = await request_gpt(session=session, text=prompt)

    await send_message(
        session=session,
        chat_id=chat_id,
        text=resp,
    )
