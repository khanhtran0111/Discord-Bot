import discord
from discord.ext import commands
import requests
from datetime import datetime

class F1Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name ="racewinner", help="Get the winners of the lastest race")
    async def race_winner(self, ctx):
        response = requests.get('http://ergast.com/api/f1/current/last/results.json')
        data = response.json()

        if response.status_code == 200 and data['MRData']['RaceTable']['Races']:
            race = data['MRData']['RaceTable']['Races'][0]
            results = race['Results']
            winner = results[0]  # The winner is the first in the results
            driver = winner['Driver']
            embed = discord.Embed(title=f"{race['raceName']} Winner", description=f"Season {race['season']}, Round {race['round']}", color=0xFFFF00)
            embed.add_field(name=f"{winner['position']}. {driver['givenName']} {driver['familyName']}", value=f"Team: {winner['Constructor']['name']}\nLaps: {winner['laps']}\nTime: {winner['Time']['time'] if 'Time' in winner else 'N/A'}", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send('No race data found for the latest race.')

    @commands.command(name ="calendar", help ="Get full calendar of the next race")
    async def next_race(self, ctx):
        response = requests.get('http://ergast.com/api/f1/current.json')
        data = response.json()

        if response.status_code == 200 and data['MRData']['RaceTable']['Races']:
            races = data['MRData']['RaceTable']['Races']
            now = datetime.now()

            for race in races:
                race_date = datetime.strptime(race['date'], '%Y-%m-%d')
                if race_date > now:
                    embed = discord.Embed(title=f"Next Race: {race['raceName']}", description=f"Season {race['season']}, Round {race['round']}", color=0xFFA500)
                    embed.add_field(name="Circuit", value=race['Circuit']['circuitName'], inline=False)
                    embed.add_field(name="Location", value=f"{race['Circuit']['Location']['locality']}, {race['Circuit']['Location']['country']}", inline=False)
                    embed.add_field(name="Date", value=race['date'], inline=False)
                    await ctx.send(embed=embed)
                    break
            else:
                await ctx.send("**No upcoming races found for the current season.**")
        else:
            await ctx.send("**No race data found for the current season.**")

    @commands.command(name ="standings", help ="Get the current driver standings")
    async def standings(self, ctx):
        response = requests.get('http://ergast.com/api/f1/current/driverStandings.json')
        data = response.json()

        if response.status_code == 200 and data['MRData']['StandingsTable']['StandingsLists']:
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            embed = discord.Embed(title="Current Driver Standings", color=0x00ff00)

            for standing in standings:
                driver = standing['Driver']
                embed.add_field(name=f"{standing['position']}. {driver['givenName']} {driver['familyName']}", value=f"Points: {standing['points']}\nWins: {standing['wins']}", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("**No driver standings found for the current season.**")

    @commands.command(name ="constructor", help ="Get the current constructor standings")
    async def constructor(self, ctx):
        response = requests.get('http://ergast.com/api/f1/current/constructorStandings.json')
        data = response.json()

        if response.status_code == 200 and data['MRData']['StandingsTable']['StandingsLists']:
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
            embed = discord.Embed(title="Current Constructor Standings", color=0x00ff00)

            for standing in standings:
                constructor = standing['Constructor']
                embed.add_field(name=f"{standing['position']}. {constructor['name']}", value=f"Points: {standing['points']}\nWins: {standing['wins']}", inline=False)

            await ctx.send(embed=embed)
        else:
            await ctx.send("**No constructor standings found for the current season.**")

    @commands.command(name ="search", help = "search information about a driver in a specific season")
    async def search(self, ctx, name: str, season: str):
        response = requests.get(f'http://ergast.com/api/f1/{season}/drivers/{name}/driverStandings.json')
        data = response.json()

        if data['MRData']['StandingsTable']['StandingsLists']:
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings'][0]
            driver = standings['Driver']
            constructor = standings['Constructors'][0]
            wins = standings['wins']
            points = standings['points']

            embed = discord.Embed(title=f"{driver['givenName']} {driver['familyName']}", description=f"Season: {season}", color=0x00ff00)
            embed.add_field(name="Team", value=constructor['name'], inline=False)
            embed.add_field(name="Wins", value=wins, inline=True)
            embed.add_field(name="Points", value=points, inline=True)

            await ctx.send(embed=embed)
        else:
            await ctx.send(f"No data found for driver {name} in season {season}")