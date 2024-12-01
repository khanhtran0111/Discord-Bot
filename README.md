# Discord-Bot

Hi, this is a template Discord bot using Python.

To use this bot, you have to go to the [Discord Developer Portal](https://discord.com/developers/applications), create a new Bot, and get the Token code.

Beside, to use weather commands, you should have your own API key.
In this code, i use API key from [OpenWeather](https://openweathermap.org/), create your account and get API key. Then replace it in `weather.py`.

You can change command prefix to whatever you want!

All your api keys, https link will be saved in .env fle, so you have to create it by your self, then configure it.

For example, this is `.env` file template:

```
BOT_COMMAND_PREFIX=!
BOT_AUTHORIZE_TOKEN=YOUR_BOT_TOKEN
OPENWEATHERMAP_API_KEY=YOUR_OPENWEATHER_API
OPENWEATHERMAP_BASE_URL=http://api.openweathermap.org/data/2.5
TIMEANDDATE_BASE_URL=https://www.timeanddate.com/weather
```

Then, if you want to create another function, use this `.env`, load it in env.py then you can run.

You can add it to your community server or your own server to use it.

## Functions of the bot

My bot has some functions to support users in the server.

I'm updating my code every month, so maybe you'll see some new functions 🤔

To show all commands, `!help` will help you to do that.

### Note

This function helps users to take notes, view notes, set reminders, and delete notes.
+ takenote: Take a note and assign it to a category. There are 4 categories: Red (highest priority level, needs to be done or executed immediately), Yellow (high priority level, important), Blue (medium priority level), and Green (low priority level).
+ viewnotes: View all notes, and you can mark them as completed.
+ deletenote: Delete a specific note from the note queue.
+ settime: Set a reminder for a specific note.
+ deleteallnotes: Delete all user's notes.
+ Updating...

### Weather
This function shows user informations about weather.
+ weather: use this command for short weather's information in that day.
+ temp: Get the weather forecast for the next week for a specific city.
+ compare: Compare the temperature forecast for the next week between two cities.

### Formula 1

This function helps users search for information about any category in Formula 1. (Forza Ferrari)
+ racewinner: Get the winner of the latest race.
+ calendar: Get the full calendar of the next race.
+ standings: Get the current driver standings.
+ constructor: Get the current constructor standings.
+ search: Get information about a driver in a specific season.
