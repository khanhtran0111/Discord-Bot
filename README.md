# Discord Bot

This is a template for a Discord bot using Python.

To use this bot, you need to visit the [Discord Developer Portal](https://discord.com/developers/applications), create a new bot, and obtain its token.

Additionally, to use the weather-related commands, you will need your own API key. In this code, I use an API key from [OpenWeather](https://openweathermap.org/). Create an account there to get your API key, then replace the placeholder in `weather.py`.

You can also customize the bot's command prefix to whatever you prefer!

All your API keys and URLs are stored in a `.env` file. You will need to create this file and configure it accordingly.

### Example `.env` File

```
BOT_COMMAND_PREFIX=!
BOT_AUTHORIZE_TOKEN=YOUR_BOT_TOKEN
OPENWEATHERMAP_API_KEY=YOUR_OPENWEATHER_API
OPENWEATHERMAP_BASE_URL=http://api.openweathermap.org/data/2.5
TIMEANDDATE_BASE_URL=https://www.timeanddate.com/weather
```


Once your `.env` file is set up, load it in your code using `dotenv`, and you're good to go.

You can add this bot to your community server or personal server for fun and functionality.

---

## Features of the Bot

This bot includes several features to support server members.  
I update the code regularly, so you might see new functions added every month! 🤔

To view all commands, type `!help` in your server.

---

### **Notes Feature**

This feature allows users to take notes, view them, set reminders, and manage notes efficiently.  
Available commands include:

- **`!takenote`**: Take a note and assign it to a category. There are 4 categories:  
  - **Red**: Highest priority, requires immediate action.  
  - **Yellow**: High priority, important tasks.  
  - **Blue**: Medium priority tasks.  
  - **Green**: Low priority tasks.

- **`!viewnotes`**: View all notes and mark them as completed.  
- **`!deletenote`**: Delete a specific note from your list.  
- **`!settime`**: Set a reminder for a specific note.  
- **`!deleteallnotes`**: Delete all your notes.  
- More features coming soon!

---

### **Weather Feature**

This feature provides users with detailed weather information.  
Available commands include:

- **`!weather`**: Get a quick weather summary for the day in a specific city.  
- **`!temp`**: Retrieve the weather forecast for the next week for a specific city.  
- **`!compare`**: Compare the weekly temperature forecasts of two cities.

---

### **Formula 1 Feature**

This feature allows users to explore various categories of Formula 1 information. (*Forza Ferrari!*)  
Available commands include:

- **`!racewinner`**: Get the winner of the latest F1 race.  
- **`!calendar`**: View the schedule for the next race.  
- **`!standings`**: Check the current driver standings.  
- **`!constructor`**: View the current constructor standings.  
- **`!search`**: Find information about a specific driver in a given season.

---
