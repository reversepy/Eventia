# bot.py

import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} ({bot.user.id})")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="people forget their own events 💀 | by Reverse"
        )
    )

    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} commands globally.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

async def load_extensions():
    extensions = [
        "cogs.create_event",
        "cogs.rsvp",
        "cogs.upcoming",
        "cogs.leaderboard",
        "cogs.reminders"
    ]
    for ext in extensions:
        try:
            await bot.load_extension(ext)
            print(f"✅ Loaded extension: {ext}")
        except Exception as e:
            print(f"❌ Failed to load {ext}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
