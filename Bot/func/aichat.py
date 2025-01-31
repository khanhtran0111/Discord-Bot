import discord
from discord.ext import commands
import requests
import os
import base64
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

class AiChat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.chat_history = {} 

    @commands.command(name="ask", help="Chat with Gemini AI (Remembers conversation context).")
    async def ask(self, ctx, *, question: str = None):
        try:
            if not GEMINI_API_KEY:
                await ctx.send("API key is not set. Please configure the .env file properly.")
                return
            
            user_id = ctx.author.id
            if user_id not in self.chat_history:
                self.chat_history[user_id] = [] 

            image_data = None
            if ctx.message.attachments:
                image_url = ctx.message.attachments[0].url
                image_data = await self.download_and_convert_image(image_url)
            
            conversation = [{"parts": [{"text": msg}]} for msg in self.chat_history[user_id][-5:]]
            conversation.append({"parts": [{"text": question if question else "What is in the image?"}]})

            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={GEMINI_API_KEY}"
            headers = {"Content-Type": "application/json"}
            
            payload = {
                "contents": conversation
            }

            if image_data:
                payload["contents"][-1]["parts"].append(
                    {
                        "inline_data": {
                            "mime_type": "image/png",
                            "data": image_data
                        }
                    }
                )

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                answer = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "I couldn't find an answer.")
                
                self.chat_history[user_id].append(f"You: {question}")
                self.chat_history[user_id].append(f"Bot: {answer}")

                await ctx.send(f"**You:** {question}\n**Bot:** {answer}")
            else:
                error_message = response.json().get("error", response.text)
                await ctx.send(
                    f"Failed to get a response from the Gemini API.\n"
                    f"**Status Code:** {response.status_code}\n"
                    f"**Error:** {error_message}"
                )
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {str(e)}")

    async def download_and_convert_image(self, image_url):
        """Downloads an image and converts it to base64 format."""
        response = requests.get(image_url)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode('utf-8')
        return None

    @commands.command(name="clear", help="Clear chat history")
    async def clear_chat(self, ctx):
        """Clear user's chat history"""
        user_id = ctx.author.id
        if user_id in self.chat_history:
            del self.chat_history[user_id]
            await ctx.send("Chat history cleared.")
        else:
            await ctx.send("No chat history found.")

def setup(bot):
    bot.add_cog(AiChat(bot))
