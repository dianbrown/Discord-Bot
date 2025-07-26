# discordBot.py
import os
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands

# 1) Load .env and grab your token
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("⚠️ BOT_TOKEN not set in .env")

# 2) Set up intents & bot
intents = discord.Intents.default()
intents.members = True  # needed to fetch voice channel members

bot = commands.Bot(command_prefix="!", intents=intents)

# 3) Define a Cog with slash commands
class VoiceMute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Check: user must be in a voice channel
    def is_in_voice_channel():
        def predicate(interaction: discord.Interaction) -> bool:
            if not (interaction.user.voice and interaction.user.voice.channel):
                raise app_commands.CheckFailure("You need to be in a voice channel.")
            return True
        return app_commands.check(predicate)

    @app_commands.command(
        name="muteall",
        description="Server-mute everyone in your current voice channel"
    )
    @app_commands.checks.has_permissions(mute_members=True)
    @is_in_voice_channel()
    async def muteall(self, interaction: discord.Interaction):
        vc = interaction.user.voice.channel
        muted, failed = [], []
        for member in vc.members:
            if member.bot:
                continue
            try:
                await member.edit(mute=True)
                muted.append(member.display_name)
            except Exception:
                failed.append(member.display_name)

        msg = f"🔇 Muted {len(muted)} members."
        if failed:
            msg += f"\n⚠️ Failed to mute: {', '.join(failed)}"
        await interaction.response.send_message(msg, ephemeral=True)

    @app_commands.command(
        name="unmuteall",
        description="Unmute everyone in your current voice channel"
    )
    @app_commands.checks.has_permissions(mute_members=True)
    @is_in_voice_channel()
    async def unmuteall(self, interaction: discord.Interaction):
        vc = interaction.user.voice.channel
        unmuted, failed = [], []
        for member in vc.members:
            if member.bot:
                continue
            try:
                await member.edit(mute=False)
                unmuted.append(member.display_name)
            except Exception:
                failed.append(member.display_name)

        msg = f"🔊 Unmuted {len(unmuted)} members."
        if failed:
            msg += f"\n⚠️ Failed to unmute: {', '.join(failed)}"
        await interaction.response.send_message(msg, ephemeral=True)

# 4) Register Cog and sync commands
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

bot.add_cog(VoiceMute(bot))

# 5) Run the bot
bot.run(TOKEN)
