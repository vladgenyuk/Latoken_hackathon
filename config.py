import os
import dotenv

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_USERNAME = os.environ.get('BOT_USERNAME')
API_KEY = os.environ.get('API_KEY')

BOT_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

ABOUT_LATOKEN_URL = 'https://latoken.me/latoken-161'

USER_STATES = {}
USER_DATA = {}

TESTS_INIT_MESSAGE = 'Этот тест будет оценивать ИИ, можешь отвечать так, как тебе удобно😊'
