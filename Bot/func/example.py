from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help=":Responds with 'pong'")
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command(name="pong", help=":Responds with 'ping'")
    async def pong(self, ctx):
        await ctx.send("ping")