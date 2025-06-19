# cogs/upcoming.py

import discord
from discord import app_commands
from discord.ext import commands
from utils.file_manager import load_json
from datetime import datetime

EVENTS_FILE = "events.json"

class UpcomingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="eventinfo", description="View full info about an event.")
    @app_commands.describe(event_id="The ID of the event to view.")
    async def event_info(self, interaction: discord.Interaction, event_id: str):
        events = load_json(EVENTS_FILE)

        if event_id not in events:
            await interaction.response.send_message("⚠️ Event not found.", ephemeral=True)
            return

        event = events[event_id]
        timestamp = datetime.fromisoformat(event["timestamp"])

        embed = discord.Embed(
            title=event["title"],
            description=event["description"],
            color=discord.Color.blurple()
        )
        embed.add_field(name="🕒 Time", value=f"<t:{int(timestamp.timestamp())}:F>")
        embed.add_field(name="📌 Event ID", value=event_id, inline=False)
        embed.set_footer(text=f"Created by user ID: {event['creator_id']}")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(UpcomingCog(bot))
