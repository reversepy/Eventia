# cogs/help.py

import discord
from discord import app_commands
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Show a list of all available commands.")
    async def help_command(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📘 Eventia Help Menu",
            description="Here’s a list of everything you can do with Eventia!",
            color=discord.Color.teal()
        )

        embed.add_field(name="🎉 Event Commands", value=(
            "`/createevent` – Create a new event\n"
            "`/editevent` – Edit your event\n"
            "`/deleteevent` – Delete an event you created\n"
            "`/eventinfo` – View detailed info about an event"
        ), inline=False)

        embed.add_field(name="✅ RSVP Commands", value=(
            "`/rsvp` – RSVP to an event\n"
            "`/cancelrsvp` – Cancel your RSVP\n"
            "`/myrsvps` – See which events you RSVPed to\n"
            "`/pingrsvps` – Ping all RSVP’d users (host/admin only)"
        ), inline=False)

        embed.add_field(name="📊 Stats & Profiles", value=(
            "`/leaderboard` – Top RSVP participants\n"
            "`/myprofile` – Your event participation stats"
        ), inline=False)

        embed.set_footer(text="Made with ❤️ by Reverse — discord.gg/nitrogang")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
