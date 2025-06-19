# cogs/reminders.py

import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
import pytz

from utils.file_manager import load_json
import os

EVENTS_FILE = "events.json"
RSVP_FILE = "rsvps.json"

class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_events.start()

    def cog_unload(self):
        self.check_events.cancel()

    @tasks.loop(minutes=1)
    async def check_events(self):
        now_utc = datetime.utcnow()
        events = load_json(EVENTS_FILE)
        rsvps = load_json(RSVP_FILE)

        for event_id, event in list(events.items()):
            try:
                event_dt = datetime.fromisoformat(event["timestamp"])
                # Trigger reminder 30 minutes before the event
                if now_utc + timedelta(minutes=30) >= event_dt > now_utc + timedelta(minutes=29):
                    channel = self.bot.get_channel(event["channel_id"])
                    guild = self.bot.get_guild(event["guild_id"])
                    if not channel or not guild:
                        continue

                    user_ids = rsvps.get(event_id, [])
                    mentions = []
                    for uid in user_ids:
                        user = guild.get_member(int(uid))
                        if user:
                            try:
                                await user.send(
                                    f"⏰ Reminder: The event **{event['title']}** starts in 30 minutes!\n"
                                    f"📍 {channel.mention} in **{guild.name}**"
                                )
                            except discord.Forbidden:
                                mentions.append(user.mention)

                    if mentions:
                        await channel.send(
                            f"🔔 Reminder: Event **{event['title']}** starts in 30 minutes!\n" +
                            "Some users couldn’t be DM’d: " + ", ".join(mentions)
                        )
            except Exception as e:
                print(f"[Reminder Error] {e}")

    @check_events.before_loop
    async def before_reminders(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(ReminderCog(bot))
