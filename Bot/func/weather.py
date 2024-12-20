import discord
from discord.ext import commands
import aiohttp
import matplotlib.pyplot as plt
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHERMAP_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
OPENWEATHERMAP_BASE_URL = os.getenv('OPENWEATHERMAP_BASE_URL')
TIMEANDDATE_BASE_URL = os.getenv('TIMEANDDATE_BASE_URL')

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_weather_data(self, city):
        async with aiohttp.ClientSession() as session:
            url = f"{OPENWEATHERMAP_BASE_URL}/forecast?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
            async with session.get(url) as response:
                data = await response.json()
                return data

    async def plot_temperature_graph(self, data):
        daily_temperatures = {}
        for entry in data['list']:
            date = datetime.fromtimestamp(entry['dt']).strftime('%d/%m/%Y')
            temperature = entry['main']['temp']
            if date not in daily_temperatures:
                daily_temperatures[date] = temperature
            else:
                if temperature > daily_temperatures[date]:
                    daily_temperatures[date] = temperature

        dates = [datetime.strptime(date, '%d/%m/%Y') for date in daily_temperatures.keys()]
        temperatures = list(daily_temperatures.values())

        plt.plot(dates, temperatures, marker='o', linestyle='-')
        plt.title('Temperature forecast for the next week')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.yticks([0, 10, 20, 30, 40, 50])
        plt.xticks(dates, [date.strftime('%d/%m/%Y') for date in dates], rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.savefig('temperature.png')

    @commands.command(name="temp", help="Get the weather forecast for the next week for a specific city.")
    async def weather(self, ctx, *, City):
        city = City.lower().replace(" ", "")
        weather_data = await self.get_weather_data(city)
        if 'list' in weather_data:
            await self.plot_temperature_graph(weather_data)
            forecast = ""
            daily_temperatures = {}
            for entry in weather_data['list']:
                date = datetime.fromtimestamp(entry['dt']).strftime('%d/%m/%Y')
                temperature = entry['main']['temp']
                if date not in daily_temperatures:
                    daily_temperatures[date] = temperature
                else:
                    if temperature > daily_temperatures[date]:
                        daily_temperatures[date] = temperature

            for date, temperature in daily_temperatures.items():
                forecast += f"{date}: {temperature}°C\n"
            
            embed = discord.Embed(title=f"Weather forecast for **{city}** for the next week", description=forecast, color=discord.Color.blue())
            file = discord.File('temperature.png', filename='temperature.png')
            embed.set_image(url="attachment://temperature.png")
            await ctx.send(embed=embed, file=file)
            plt.clf()
        else:
            await ctx.send(f"Couldn't fetch weather data for {city}. Please try again later.")

    async def plot_temperature_comparison(self, weather_data_city1, weather_data_city2, label1, label2):
        daily_temperatures_city1 = {}
        daily_temperatures_city2 = {}
        
        for entry in weather_data_city1['list']:
            date = datetime.fromtimestamp(entry['dt']).strftime('%d/%m/%Y')
            temperature = entry['main']['temp']
            if date not in daily_temperatures_city1:
                daily_temperatures_city1[date] = temperature
            else:
                if temperature > daily_temperatures_city1[date]:
                    daily_temperatures_city1[date] = temperature
                    
        for entry in weather_data_city2['list']:
            date = datetime.fromtimestamp(entry['dt']).strftime('%d/%m/%Y')
            temperature = entry['main']['temp']
            if date not in daily_temperatures_city2:
                daily_temperatures_city2[date] = temperature
            else:
                if temperature > daily_temperatures_city2[date]:
                    daily_temperatures_city2[date] = temperature
        
        dates = [datetime.strptime(date, '%d/%m/%Y') for date in daily_temperatures_city1.keys()]
        temperatures_city1 = list(daily_temperatures_city1.values())
        temperatures_city2 = [daily_temperatures_city2[date] for date in daily_temperatures_city1.keys()] # Use dates from city1 for consistency
        
        plt.plot(dates, temperatures_city1, marker='o', linestyle='-', label=label1)
        plt.plot(dates, temperatures_city2, marker='o', linestyle='-', label=label2)
        plt.title('Temperature forecast for the next week')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.yticks([0, 10, 20, 30, 40, 50])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.legend()

    @commands.command(name="compare", help="Compare the temperature forecast for the next week between two cities.")
    async def compare(self, ctx, *, cities):
        city1, city2 = cities.split()
        weather_data_city1 = await self.get_weather_data(city1)
        weather_data_city2 = await self.get_weather_data(city2)
        
        if 'list' in weather_data_city1 and 'list' in weather_data_city2:
            await self.plot_temperature_comparison(weather_data_city1, weather_data_city2, city1, city2)
            plt.savefig('temperature_comparison.png')
            
            embed = discord.Embed(title=f"Temperature forecast comparison between **{city1}** and **{city2}** for the next week", color=discord.Color.blue())
            file = discord.File('temperature_comparison.png', filename='temperature_comparison.png')
            embed.set_image(url="attachment://temperature_comparison.png")
            await ctx.send(embed=embed, file=file)
            
            plt.clf()
        else:
            await ctx.send(f"Couldn't fetch weather data for one or both cities. Please try again later.")

    @commands.command(name="weather", help="Get weather information in your location")
    async def informations(self, ctx, *, location):
        city_formatted = location.lower().replace(" ", "")

        weather_data = await self.get_weather_data(location)
        if 'list' in weather_data:
            current_weather = weather_data['list'][0]
            temperature = current_weather['main']['temp']
            feels_like = current_weather['main']['feels_like']
            humidity = current_weather['main']['humidity']
            wind_speed = current_weather['wind']['speed']
            description = current_weather['weather'][0]['description']

            embed = discord.Embed(
                title=f"Weather in {location.capitalize()}",
                description=(
                    f"**Temperature**: {temperature}°C\n"
                    f"**Feels Like**: {feels_like}°C\n"
                    f"**Condition**: {description.capitalize()}\n"
                    f"**Humidity**: {humidity}%\n"
                    f"**Wind Speed**: {wind_speed} m/s"
                ),
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"Couldn't fetch weather data for {location}. Please try again later.")

