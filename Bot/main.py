import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from library import *

load_dotenv()

BOT_COMMAND_PREFIX = os.getenv('BOT_COMMAND_PREFIX')
BOT_AUTHORIZE_TOKEN = os.getenv('BOT_AUTHORIZE_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_COMMAND_PREFIX, intents=intents, help_command=commands.DefaultHelpCommand(no_category='Commands'))

def check_exist_command(bot, command_name): 
    if bot.get_command(command_name):
        return True
    return False

async def setup_command(bot, config_list):
    for config_name in config_list:
        config = config_name(bot)
        command_list = [_.name for _ in config.get_commands()]
        for command_name in command_list:
            if check_exist_command(bot, command_name):
                exit(f"Command: {command_name} already exists!")
        await bot.add_cog(config)

@bot.event
async def on_ready():
    print("Bot is running!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    IS_COMMAND = message.content.startswith(bot.command_prefix)
    if IS_COMMAND:
        command_name = message.content[len(bot.command_prefix):].split()[0]
        if not check_exist_command(bot, command_name):
            await message.channel.send(f"Command '{command_name}' does not exist.")
            return

    await bot.process_commands(message)

async def main():
    # Add your custom cogs here
    await setup_command(bot, [WeatherCog, F1Cog, NoteCog, PingCog, AiChat])
    await bot.start(BOT_AUTHORIZE_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())