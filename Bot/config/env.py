from func.example import PingCog
from func.note import NoteCog
from func.formula1 import F1Cog
from func.weather import WeatherCog

BOT_AUTHORIZE_TOKEN="YOUR_TOKEN"
BOT_COMMAND_PREFIX="!"

BOT_CONFIG_LIST = [PingCog, NoteCog, F1Cog, WeatherCog]