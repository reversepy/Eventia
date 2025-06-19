# cogs/leaderboard.py

import discord
from discord.ext import commands
from discord import app_commands
from utils.file_manager import load_json
from collections import defaultdict

RSVP_FILE = "rsvps.json"

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="leaderboard", description="See the most active event participants")
    async def leaderboard(self, interaction: discord.Interaction):
        rsvps = load_json(RSVP_FILE, default={})
        counter = defaultdict(int)

        # Count RSVP appearances
        for user_ids in rsvps.values():
            for uid in user_ids:
                counter[uid] += 1

        if not counter:
            return await interaction.response.send_message("📭 No RSVP data found.", ephemeral=True)

        sorted_users = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        top = sorted_users[:10]

        embed = discord.Embed(
            title="🏆 Event Leaderboard",
            description="Top participants by RSVP count",
            color=discord.Color.purple()
        )

        for i, (uid, count) in enumerate(top, start=1):
            try:
                user = await self.bot.fetch_user(int(uid))
                name = f"{user.name}#{user.discriminator}"
            except:
                name = f"User {uid}"
            embed.add_field(name=f"{i}. {name}", value=f"🎟️ {count} RSVPs", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(LeaderboardCog(bot))
