import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
ENDPOINT_URL = os.getenv('ENDPOINT_URL')

class GeminiCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask", help="Ask a question and get a response from the Gemini API")
    async def ask(self, ctx, *, question):
        try:
            if not GEMINI_API_KEY or not ENDPOINT_URL:
                await ctx.send("API key or endpoint URL is not set. Please configure the .env file properly.")
                return

            url = ENDPOINT_URL
            headers = {
                "Authorization": f"Bearer {GEMINI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "prompt": question
            }

            # Make a POST request to the API
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                # Parse the response and send the answer
                data = response.json()
                answer = data.get("content", "No answer found.")
                await ctx.send(f"**Question:** {question}\n**Answer:** {answer}")
            else:
                # Provide detailed error information
                error_message = response.text
                await ctx.send(
                    f"Failed to get a response from the Gemini API.\n"
                    f"**Status Code:** {response.status_code}\n"
                    f"**Error:** {error_message}"
                )
        except Exception as e:
            # Catch unexpected errors and provide feedback
            await ctx.send(f"An unexpected error occurred: {str(e)}")

# Function to add the Cog to the bot
def setup(bot):
    bot.add_cog(GeminiCog(bot))
