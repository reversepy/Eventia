# cogs/create_event.py

import discord
from discord import app_commands
from discord.ext import commands
import uuid
from datetime import datetime
from utils.file_manager import load_json, save_json

EVENTS_FILE = "events.json"

class CreateEventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="createevent", description="Create a new event.")
    @app_commands.describe(title="Title of the event", description="What is this event about?", time="When does it start? (YYYY-MM-DD HH:MM)")
    async def create_event(self, interaction: discord.Interaction, title: str, description: str, time: str):
        try:
            dt = datetime.strptime(time, "%Y-%m-%d %H:%M")
        except ValueError:
            await interaction.response.send_message("⏰ Invalid time format. Use `YYYY-MM-DD HH:MM` (24h).", ephemeral=True)
            return

        events = load_json(EVENTS_FILE)
        event_id = str(uuid.uuid4())[:8]

        events[event_id] = {
            "title": title,
            "description": description,
            "timestamp": dt.isoformat(),
            "creator_id": interaction.user.id,
            "channel_id": interaction.channel_id,
            "guild_id": interaction.guild_id,
        }

        save_json(EVENTS_FILE, events)

        await interaction.response.send_message(
            f"✅ Event **{title}** created!\n"
            f"🆔 ID: `{event_id}`\n"
            f"🕒 Starts: <t:{int(dt.timestamp())}:F>\n"
            f"📜 Description: {description}"
        )

    @app_commands.command(name="deleteevent", description="Delete an event you created.")
    @app_commands.describe(event_id="The ID of the event to delete.")
    async def delete_event(self, interaction: discord.Interaction, event_id: str):
        events = load_json(EVENTS_FILE)

        if event_id not in events:
            await interaction.response.send_message("⚠️ Event not found.", ephemeral=True)
            return

        event = events[event_id]
        if interaction.user.id != event["creator_id"] and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("🚫 You don't have permission to delete this event.", ephemeral=True)
            return

        del events[event_id]
        save_json(EVENTS_FILE, events)

        await interaction.response.send_message(f"🗑️ Event `{event_id}` has been deleted.", ephemeral=True)

    @app_commands.command(name="editevent", description="Edit an existing event you created.")
    @app_commands.describe(event_id="The event ID to edit", new_title="New title (optional)", new_description="New description (optional)", new_time="New time (optional, format: YYYY-MM-DD HH:MM)")
    async def edit_event(self, interaction: discord.Interaction, event_id: str, new_title: str = None, new_description: str = None, new_time: str = None):
        events = load_json(EVENTS_FILE)

        if event_id not in events:
            await interaction.response.send_message("⚠️ Event not found.", ephemeral=True)
            return

        event = events[event_id]
        if interaction.user.id != event["creator_id"] and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("🚫 You don't have permission to edit this event.", ephemeral=True)
            return

        if new_title:
            event["title"] = new_title
        if new_description:
            event["description"] = new_description
        if new_time:
            try:
                dt = datetime.strptime(new_time, "%Y-%m-%d %H:%M")
                event["timestamp"] = dt.isoformat()
            except ValueError:
                await interaction.response.send_message("⏰ Invalid time format. Use `YYYY-MM-DD HH:MM` (24h).", ephemeral=True)
                return

        events[event_id] = event
        save_json(EVENTS_FILE, events)
        await interaction.response.send_message(f"✏️ Event `{event_id}` has been updated.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CreateEventCog(bot))
