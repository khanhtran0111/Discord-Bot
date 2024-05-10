import discord
import asyncio
from discord.ext import commands
from collections import defaultdict
import json
import aiofiles
from datetime import datetime

# Emoji representations for note categories
CATEGORY_EMOJIS = {
    "red": "🔴",
    "yellow": "🟡",
    "blue": "🔵",
    "green": "🟢"
}

# Ordered list of emojis for sorting purposes
CATEGORY_ORDER = ["🔴", "🟡", "🔵", "🟢"]
# Emoji for marking a note as completed
GREEN_TICK_EMOJI = "✅"

class NoteCog(commands.Cog):
    ''' 
    NoteCog: A Discord bot cog for managing notes.

    Usage
    -----
    This cog allows users to take notes, view all notes, mark notes as completed, delete specific notes, and set reminders for notes.

    Commands
    --------
    takenote: Take a note and assign it to a category.
    viewnotes: View all notes and mark them as completed.
    deletenote: Delete a specific note from the note queue.
    settime: Set a reminder for a specific note.
    '''
    def __init__(self, bot):
        ''' 
        Initialize the NoteCog class.

        Parameters
        ----------
        bot (discord.ext.commands.Bot): The Discord bot instance.
        '''
        self.bot = bot
        self.user_notes = defaultdict(list)  # Stores notes per user in a defaultdict
        self.reminders = {}  # Stores reminders for notes
        asyncio.create_task(self.load_notes())  # Asynchronously load notes at bot startup

    async def load_notes(self):
        '''Load notes and reminders from a JSON file asynchronously.'''
        try:
            async with aiofiles.open('user_data.json', 'r') as f:
                data = json.loads(await f.read())
                self.user_notes = data.get('user_notes', defaultdict(list))
                self.reminders = data.get('reminders', {})
        except FileNotFoundError:
            # Initialize to empty defaultdict if file doesn't exist
            pass
        except json.JSONDecodeError as e:
            # Log any JSON errors encountered during file reading
            print(f"Failed to decode JSON: {e}")

    async def save_notes(self):
        '''Save the current notes and reminders to a JSON file asynchronously.'''
        data = {
            'user_notes': self.user_notes,
            'reminders': self.reminders
        }
        try:
            async with aiofiles.open('user_data.json', 'w') as f:
                await f.write(json.dumps(data, indent=4))
        except IOError as e:
            # Log any IO errors encountered during file writing
            print(f"Failed to write data to file: {e}")


    async def __print_remaining_notes(self, ctx):
        '''Helper method to display remaining notes for a user.'''
        user_id = str(ctx.author.id)
        if not self.user_notes[user_id]:
            await ctx.send("No notes available")
            return
        
        notes_display = "\n".join(f"{idx}. {emoji}: {note}" for idx, (emoji, note) in enumerate(self.user_notes[user_id], 1))
        await ctx.send(f"{ctx.author.mention}'s new notes:\n{notes_display}")

    @commands.command(name="takenote", help="Take a note and assign it to a category.")
    async def take_note(self, ctx, *, note: str = None):
        '''
        Usage
        ----- 
        Take a note and assign it to a category.

        Parameters
        ----------
        ctx (discord.ext.commands.Context): The context in which the command was invoked.
        note (string, optional): The note to be taken. Defaults to None.
        '''
        if not note:
            await ctx.send("**Please provide a note**.")
            return
        
        user_id = str(ctx.author.id)
        note_message = await ctx.send(f'**Note added**: {note}\nPlease select your category:')
        for emoji in CATEGORY_EMOJIS.values():
            await note_message.add_reaction(emoji)
        
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in CATEGORY_EMOJIS.values()
        
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
            category = next(key for key, value in CATEGORY_EMOJIS.items() if value == reaction.emoji)
            self.user_notes[user_id].append((reaction.emoji, note))
            await self.save_notes()
            await ctx.send(f'**Note added to category** {reaction.emoji}: {note}')
        except asyncio.TimeoutError:
            await ctx.send("**Timed out. No category selected**.")

    @commands.command(name="viewnotes", help="View all notes and mark them as completed.")
    async def view_note(self, ctx):
        '''
        Usage
        ----- 
        View all notes and mark them as completed.

        Parameters
        ----------
        ctx (discord.ext.commands.Context): The context in which the command was invoked.
        '''
        user_id = str(ctx.author.id)
        if not self.user_notes[user_id]:
            await ctx.send("**No notes available**")
            return

        await ctx.send(f"{ctx.author.mention}\n# Notes:")

        sorted_notes = sorted(self.user_notes[user_id], key=lambda x: CATEGORY_ORDER.index(x[0]))
        self.note_messages = {}

        for note_index, (emoji, note) in enumerate(sorted_notes, 1):
            message = await ctx.send(f"{note_index}. {emoji}: {note}")
            self.note_messages[message.id] = emoji
            await message.add_reaction(GREEN_TICK_EMOJI)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == GREEN_TICK_EMOJI and reaction.message.id in self.note_messages

        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=180.0, check=check)
            await ctx.send("Note completed. ✅")
            message_id = reaction.message.id
            if message_id in self.note_messages:
                category_to_remove = self.note_messages.pop(message_id)
                self.user_notes[user_id] = [note for note in self.user_notes[user_id] if note[0] != category_to_remove]
                await self.save_notes()
                await reaction.message.delete()
                await self.__print_remaining_notes(ctx)
        except asyncio.TimeoutError:
            await ctx.send("")

    @commands.command(name="deletenote", help="Delete a specific note.")
    async def delete_note(self, ctx, note_number: int):
        '''
        Usage
        ----- 
        Delete a specific note from the note queue.

        Parameters
        ----------
        ctx (discord.ext.commands.Context): The context in which the command was invoked.
        note_number (int): The number of the note to be deleted.
        '''
        user_id = str(ctx.author.id)
        if not self.user_notes[user_id]:
            await ctx.send("**No notes available**")
            return

        if 1 <= note_number <= len(self.user_notes[user_id]):
            deleted_note = self.user_notes[user_id].pop(note_number - 1)
            await self.save_notes()
            await ctx.send(f'**Note deleted**: {deleted_note[1]}')
            await self.__print_remaining_notes(ctx)
        else:
            await ctx.send("Invalid note number provided.")

    @commands.command(name="settime", help="Set a reminder for a specific note.")
    async def set_reminder(self, ctx, note_number: int, reminder_date: str, reminder_time: str):
        '''
        Set a reminder for a specific note.

        Parameters
        ----------
        ctx (discord.ext.commands.Context): The context in which the command was invoked.
        note_number (int): The number of the note for which the reminder is set.
        reminder_date (str): The date of the reminder in format DD/MM/YYYY.
        reminder_time (str): The time of the reminder in 24-hour format HH:MM.
        '''
        user_id = str(ctx.author.id)
        if not self.user_notes[user_id]:
            await ctx.send("**No notes available**")
            return

        if 1 <= note_number <= len(self.user_notes[user_id]):
            note = self.user_notes[user_id][note_number - 1][1]
            reminder_datetime = datetime.strptime(f"{reminder_date} {reminder_time}", "%d/%m/%Y %H:%M")
            await ctx.send(f"**Reminder set for note** {note_number}: {note} **on** {reminder_datetime.strftime('%d/%m/%Y %H:%M')}")
            # Add reminder to user's reminders
            if user_id not in self.reminders:
                self.reminders[user_id] = {}
            self.reminders[user_id][note_number] = (ctx.channel.id, note, reminder_datetime)
            await self.save_notes()
            asyncio.create_task(self.send_reminder(user_id, ctx.channel.id, note, reminder_datetime))
        else:
            await ctx.send("**Invalid note number provided**.")

    async def send_reminder(self, channel_id, note, reminder_datetime):
        '''Send reminder to the user at the specified datetime.'''
        current_datetime = datetime.now()
        delta = (reminder_datetime - current_datetime).total_seconds()
        await asyncio.sleep(delta)
        channel = self.bot.get_channel(channel_id)
        if channel:
            await channel.send(f"**Reminder**: {note}")


