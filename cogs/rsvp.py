# cogs/rsvp.py

import discord
from discord import app_commands
from discord.ext import commands
import datetime
from utils.file_manager import load_json, save_json

EVENTS_FILE = "events.json"
RSVP_FILE = "rsvps.json"

class RSVPCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rsvp", description="RSVP to an event.")
    @app_commands.describe(event_id="The ID of the event you want to RSVP to.")
    async def rsvp(self, interaction: discord.Interaction, event_id: str):
        events = load_json(EVENTS_FILE)
        rsvps = load_json(RSVP_FILE)

        if event_id not in events:
            await interaction.response.send_message("⚠️ That event doesn't exist.", ephemeral=True)
            return

        user_id = str(interaction.user.id)
        rsvps.setdefault(event_id, [])
        if user_id not in rsvps[event_id]:
            rsvps[event_id].append(user_id)
            save_json(RSVP_FILE, rsvps)
            await interaction.response.send_message("✅ You've RSVPed to the event!")
        else:
            await interaction.response.send_message("❗ You're already RSVPed.", ephemeral=True)

    @app_commands.command(name="cancelrsvp", description="Cancel your RSVP for an event.")
    @app_commands.describe(event_id="The ID of the event you want to cancel RSVP for.")
    async def cancel_rsvp(self, interaction: discord.Interaction, event_id: str):
        rsvps = load_json(RSVP_FILE)
        user_id = str(interaction.user.id)

        if event_id not in rsvps or user_id not in rsvps[event_id]:
            await interaction.response.send_message("❌ You haven't RSVPed to that event.", ephemeral=True)
            return

        rsvps[event_id].remove(user_id)
        if not rsvps[event_id]:
            del rsvps[event_id]
        save_json(RSVP_FILE, rsvps)
        await interaction.response.send_message("✅ Your RSVP has been removed.", ephemeral=True)

    @app_commands.command(name="myrsvps", description="See which events you have RSVPed to.")
    async def my_rsvps(self, interaction: discord.Interaction):
        rsvps = load_json(RSVP_FILE)
        events = load_json(EVENTS_FILE)
        user_id = str(interaction.user.id)

        user_events = [
            f"📌 **{events[eid]['title']}** — <t:{int(datetime.datetime.fromisoformat(events[eid]['timestamp']).timestamp())}:F>"
            for eid in rsvps
            if user_id in rsvps[eid] and eid in events
        ]

        if not user_events:
            await interaction.response.send_message("🙅‍♂️ You're not RSVPed to any events.", ephemeral=True)
            return

        await interaction.response.send_message(
            "**📅 Your RSVP'd Events:**\n" + "\n".join(user_events),
            ephemeral=True
        )

    @app_commands.command(name="pingrsvps", description="Ping all RSVP’d users for an event.")
    @app_commands.describe(event_id="The ID of the event to ping users for.")
    async def ping_rsvps(self, interaction: discord.Interaction, event_id: str):
        events = load_json(EVENTS_FILE)
        rsvps = load_json(RSVP_FILE)

        if event_id not in events:
            await interaction.response.send_message("⚠️ Event not found.", ephemeral=True)
            return

        event = events[event_id]
        if interaction.user.id != event["creator_id"] and not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message("🚫 You don't have permission to ping RSVP’d users for this event.", ephemeral=True)
            return

        user_ids = rsvps.get(event_id, [])
        mentions = [f"<@{uid}>" for uid in user_ids]

        if not mentions:
            await interaction.response.send_message("❌ No RSVP’d users to ping.", ephemeral=True)
            return

        await interaction.response.send_message(
            f"📣 Pinging RSVP’d users for **{event['title']}**:\n" + " ".join(mentions)
        )

async def setup(bot):
    await bot.add_cog(RSVPCog(bot))
