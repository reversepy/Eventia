# cogs/events.py

import discord
from discord.ext import commands
from discord import app_commands
import uuid
from datetime import datetime, timedelta
import pytz

from utils.file_manager import load_json, save_json

EVENTS_FILE = "events.json"

class EventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events = load_json(EVENTS_FILE, default={})

    def save(self):
        save_json(EVENTS_FILE, self.events)

    @app_commands.command(name="createevent", description="Create a new server event")
    @app_commands.describe(
        title="Title of the event",
        description="Description of the event",
        datetime_str="When is it? Format: YYYY-MM-DD HH:MM (24hr)",
        timezone="Timezone (e.g., UTC, US/Eastern)",
        channel="Channel to post the event in"
    )
    async def create_event(
        self,
        interaction: discord.Interaction,
        title: str,
        description: str,
        datetime_str: str,
        timezone: str,
        channel: discord.TextChannel
    ):
        try:
            tz = pytz.timezone(timezone)
        except pytz.UnknownTimeZoneError:
            return await interaction.response.send_message("❌ Invalid timezone.", ephemeral=True)

        try:
            naive_dt = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            event_dt = tz.localize(naive_dt)
        except ValueError:
            return await interaction.response.send_message("❌ Invalid datetime format. Use `YYYY-MM-DD HH:MM`.", ephemeral=True)

        event_id = str(uuid.uuid4())[:8]

        self.events[event_id] = {
            "id": event_id,
            "title": title,
            "description": description,
            "timestamp": event_dt.isoformat(),
            "timezone": timezone,
            "channel_id": channel.id,
            "guild_id": interaction.guild_id,
            "creator_id": interaction.user.id
        }

        self.save()

        embed = discord.Embed(
            title=f"📅 {title}",
            description=description,
            color=discord.Color.blue()
        )
        embed.add_field(name="🕒 When", value=f"{event_dt.strftime('%Y-%m-%d %H:%M')} ({timezone})", inline=False)
        embed.add_field(name="📍 Where", value=channel.mention, inline=False)
        embed.set_footer(text=f"Event ID: {event_id}")

        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Event created and posted in {channel.mention}!", ephemeral=True)

    @app_commands.command(name="upcoming", description="See upcoming events")
    async def upcoming_events(self, interaction: discord.Interaction):
        now = datetime.utcnow()
        upcoming = []

        for event in self.events.values():
            event_dt = datetime.fromisoformat(event["timestamp"])
            if event_dt > now and event["guild_id"] == interaction.guild_id:
                upcoming.append((event_dt, event))

        if not upcoming:
            return await interaction.response.send_message("📭 No upcoming events found.", ephemeral=True)

        upcoming.sort(key=lambda x: x[0])
        embed = discord.Embed(
            title="📆 Upcoming Events",
            color=discord.Color.green()
        )

        for event_dt, event in upcoming[:5]:
            embed.add_field(
                name=f"{event['title']} ({event_dt.strftime('%Y-%m-%d %H:%M')})",
                value=f"{event['description']}\n📍 <#{event['channel_id']}>",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(EventCog(bot))
