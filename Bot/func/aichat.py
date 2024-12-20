import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

class AiChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask", help="Ask a question and get a response from the Gemini API")
    async def ask(self, ctx, *, question: str):
        try:
            if not GEMINI_API_KEY:
                await ctx.send("API key is not set. Please configure the .env file properly.")
                return

            url = "https://actual-gemini-api-endpoint.com/v1/chat"

            headers = {
                "Authorization": f"Bearer {GEMINI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {"prompt": question}

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                answer = data.get("content", "I couldn't find an answer.")
                await ctx.send(f"**Question:** {question}\n**Answer:** {answer}")
            else:
                error_message = response.json().get("error", response.text)
                await ctx.send(
                    f"Failed to get a response from the Gemini API.\n"
                    f"**Status Code:** {response.status_code}\n"
                    f"**Error:** {error_message}"
                )
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {str(e)}")

def setup(bot):
    bot.add_cog(AiChat(bot))
