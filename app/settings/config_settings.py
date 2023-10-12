import os
import dotenv
from pathlib import Path

from aiogram import Dispatcher, Router, Bot

BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR, ".env")

if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# bot
token = os.environ['BOT_TOKEN']
dp = Dispatcher()
router = Router()
bot = Bot(token)


# bd_settings
host = os.environ['HOST']
user = os.environ['USER']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
port = os.environ["PORT"]
db_url = os.environ["DB_URL"]
