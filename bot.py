# bot.py

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Needed if using message content later
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")

# Load cogs
initial_cogs = ["cogs.events", "cogs.rsvp", "cogs.leaderboard"]
for cog in initial_cogs:
    bot.load_extension(cog)

bot.run(os.getenv("DISCORD_TOKEN"))
