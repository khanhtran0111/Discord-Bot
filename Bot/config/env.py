import os
from func.example import PingCog
from func.note import NoteCog
from func.formula1 import F1Cog
from func.weather import WeatherCog
from func.gemini import GeminiCog
from dotenv import load_dotenv

load_dotenv()

BOT_COMMAND_PREFIX = os.getenv('BOT_COMMAND_PREFIX')
BOT_AUTHORIZE_TOKEN = os.getenv('BOT_AUTHORIZE_TOKEN')
OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
OPENWEATHERMAP_BASE_URL = os.getenv('OPENWEATHERMAP_BASE_URL')
TIMEANDDATE_BASE_URL = os.getenv('TIMEANDDATE_BASE_URL')
ERGAST_API_BASE_URL = os.getenv('ERGAST_API_BASE_URL')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')