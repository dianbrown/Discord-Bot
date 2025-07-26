# discordBot.py
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# 1) Load .env and grab your token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if TOKEN is None:
    raise RuntimeError("⚠️ BOT_TOKEN not set in .env")

# 2) Set up intents & bot
intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

# 3) Define your events & commands
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")

def is_in_voice_channel():
    async def predicate(ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            return True
        await ctx.send("❌ You need to be in a voice channel.")
        return False
    return commands.check(predicate)

@bot.command()
@commands.has_permissions(mute_members=True)
@is_in_voice_channel()
async def muteall(ctx):
    vc = ctx.author.voice.channel
    muted, failed = [], []
    for m in vc.members:
        if m.bot: continue
        try:
            await m.edit(mute=True)
            muted.append(m.display_name)
        except:
            failed.append(m.display_name)
    await ctx.send(f"🔇 Muted {len(muted)} users." +
                   (f"\n⚠️ Failed: {', '.join(failed)}" if failed else ""))

@bot.command()
@commands.has_permissions(mute_members=True)
@is_in_voice_channel()
async def unmuteall(ctx):
    vc = ctx.author.voice.channel
    unm, failed = [], []
    for m in vc.members:
        if m.bot: continue
        try:
            await m.edit(mute=False)
            unm.append(m.display_name)
        except:
            failed.append(m.display_name)
    await ctx.send(f"🔊 Unmuted {len(unm)} users." +
                   (f"\n⚠️ Failed: {', '.join(failed)}" if failed else ""))

@bot.command(name="help")
async def help_cmd(ctx):
    await ctx.send(
        "**Voice‑Mute Bot Commands**\n"
        "`!muteall`  – server‑mute everyone in your voice channel\n"
        "`!unmuteall` – unmute everyone in your voice channel\n"
    )

# 4) Finally, run
bot.run(TOKEN)
