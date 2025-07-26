# discordBot.py
import os
from pathlib import Path
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord import app_commands

# 1) Load .env
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)
TOKEN    = os.getenv("BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
if not TOKEN or not GUILD_ID:
    raise RuntimeError("BOT_TOKEN and GUILD_ID must be set in .env")

GUILD = discord.Object(id=int(GUILD_ID))

# 2) Subclass Bot to use setup_hook
class MuteBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(
            command_prefix="!", 
            intents=intents,
            application_id=int(os.getenv("APPLICATION_ID", 0)),  # optional but recommended
        )

    async def setup_hook(self):
        # register Cogs
        await self.add_cog(VoiceMute(self))
        # register slash commands to your guild
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)
        print("🔄 Commands synced to guild", GUILD_ID)

    async def on_ready(self):
        print(f"✅ Logged in as {self.user} (ID: {self.user.id})")

# 3) Your Cog
class VoiceMute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def is_in_voice_channel():
        def predicate(interaction: discord.Interaction) -> bool:
            if not (interaction.user.voice and interaction.user.voice.channel):
                raise app_commands.CheckFailure("You need to be in a voice channel.")
            return True
        return app_commands.check(predicate)

    @app_commands.command(
        name="muteall",
        description="Server‑mute everyone in your current voice channel"
    )
    @app_commands.checks.has_permissions(mute_members=True)
    @is_in_voice_channel()
    async def muteall(self, interaction: discord.Interaction):
        vc = interaction.user.voice.channel
        muted, failed = [], []
        for m in vc.members:
            if m.bot: continue
            try:
                await m.edit(mute=True)
                muted.append(m.display_name)
            except:
                failed.append(m.display_name)
        reply = f"🔇 Muted {len(muted)} members."
        if failed:
            reply += f"\n⚠️ Failed: {', '.join(failed)}"
        await interaction.response.send_message(reply, ephemeral=True)

    @app_commands.command(
        name="unmuteall",
        description="Unmute everyone in your current voice channel"
    )
    @app_commands.checks.has_permissions(mute_members=True)
    @is_in_voice_channel()
    async def unmuteall(self, interaction: discord.Interaction):
        vc = interaction.user.voice.channel
        unm, failed = [], []
        for m in vc.members:
            if m.bot: continue
            try:
                await m.edit(mute=False)
                unm.append(m.display_name)
            except:
                failed.append(m.display_name)
        reply = f"🔊 Unmuted {len(unm)} members."
        if failed:
            reply += f"\n⚠️ Failed: {', '.join(failed)}"
        await interaction.response.send_message(reply, ephemeral=True)

# 4) Run it
bot = MuteBot()
bot.run(TOKEN)
