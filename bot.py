# bot.py

import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.members = True  # needed if you fetch user info
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)
TOKEN = "YOUR_BOT_TOKEN"  # Replace with your actual token

@bot.event
async def on_ready():
    print(f"🟢 Logged in as {bot.user} (ID: {bot.user.id})")
    print("🔁 Syncing slash commands...")
    await bot.tree.sync()
    print("✅ Slash commands synced.")

    # Optional funny status
    await bot.change_presence(activity=discord.Game(name="🗓️ planning events | by Reverse"))

# Auto-load all cogs in the cogs/ folder
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded cog: {filename}")
            except Exception as e:
                print(f"❌ Failed to load {filename}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

asyncio.run(main())
