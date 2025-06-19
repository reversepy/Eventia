# cogs/rsvp.py

import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
from utils.file_manager import load_json, save_json

import os
from datetime import datetime

EVENTS_FILE = "events.json"
RSVP_FILE = "rsvps.json"

class RSVPView(View):
    def __init__(self, event_id, bot):
        super().__init__(timeout=None)
        self.event_id = event_id
        self.bot = bot

        self.add_item(RSVPButton(event_id, bot))

class RSVPButton(Button):
    def __init__(self, event_id, bot):
        super().__init__(label="✅ RSVP", style=discord.ButtonStyle.success)
        self.event_id = event_id
        self.bot = bot

    async def callback(self, interaction: discord.Interaction):
        rsvps = load_json(RSVP_FILE, default={})
        user_id = str(interaction.user.id)

        if self.event_id not in rsvps:
            rsvps[self.event_id] = []

        if user_id in rsvps[self.event_id]:
            await interaction.response.send_message("❗ You've already RSVPed for this event!", ephemeral=True)
        else:
            rsvps[self.event_id].append(user_id)
            save_json(RSVP_FILE, rsvps)
            await interaction.response.send_message("🎉 You're now RSVPed!", ephemeral=True)


class RSVPCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events = load_json(EVENTS_FILE, default={})

    @app_commands.command(name="postrsvp", description="Post the RSVP button for an event")
    @app_commands.describe(event_id="The short event ID you got when creating it")
    async def post_rsvp(self, interaction: discord.Interaction, event_id: str):
        event = self.events.get(event_id)
        if not event or event["guild_id"] != interaction.guild_id:
            return await interaction.response.send_message("❌ Event not found.", ephemeral=True)

        channel = self.bot.get_channel(event["channel_id"])
        if not channel:
            return await interaction.response.send_message("❌ Channel not found.", ephemeral=True)

        embed = discord.Embed(
            title=f"📅 {event['title']}",
            description=event['description'],
            color=discord.Color.blurple()
        )
        embed.add_field(name="🕒 When", value=f"{event['timestamp'][:16].replace('T', ' ')} ({event['timezone']})", inline=False)
        embed.set_footer(text=f"Event ID: {event_id}")

        view = RSVPView(event_id, self.bot)
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"📨 RSVP posted to {channel.mention}!", ephemeral=True)

    @app_commands.command(name="rsvplist", description="Show who RSVPed to an event")
    @app_commands.describe(event_id="The short event ID")
    async def rsvp_list(self, interaction: discord.Interaction, event_id: str):
        rsvps = load_json(RSVP_FILE, default={})
        event_rsvps = rsvps.get(event_id, [])

        if not event_rsvps:
            return await interaction.response.send_message("📭 No RSVPs yet for this event.", ephemeral=True)

        names = []
        for user_id in event_rsvps:
            user = await self.bot.fetch_user(int(user_id))
            names.append(f"• {user.name}#{user.discriminator}")

        embed = discord.Embed(
            title="🎟️ RSVP List",
            description="\n".join(names),
            color=discord.Color.gold()
        )
        embed.set_footer(text=f"Event ID: {event_id}")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(RSVPCog(bot))
