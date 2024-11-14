import discord
from discord.ext import commands
import asyncio
from datetime import timedelta
from discord.utils import utcnow
import time
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent if your bot processes messages
intents.voice_states = True     # Enable voice states for voice channel events

bot = commands.Bot(command_prefix='/', intents=intents)
polls = {}

@bot.command(name="bye")
async def bye(ctx, username: str):
    excluded_user_ids = {272937604339466240, 412347553141751808}
    member = discord.utils.get(ctx.guild.members, name=username)
    if not member:
        await ctx.send(f"User {username} not found.")
        return

    if ctx.author.voice and ctx.author.voice.channel and (len(ctx.author.voice.channel.members) > 2):
        voice_channel = ctx.author.voice.channel
        voice_client = await voice_channel.connect()    

        members = [member for member in voice_channel.members if member.id not in excluded_user_ids]
        non_excluded_count = len(members)

        # Start the poll
        polls[ctx.guild.id] = {"target": member, "votes": set(), "voice_client": voice_client}

        await ctx.send(f"A poll has started to timeout {username}. Type 'yes' in this channel to vote.")

        # Wait for the poll to complete
        while len(polls[ctx.guild.id]["votes"]) < (len(voice_channel.non_excluded_count) - 2):
            try:
                message = await bot.wait_for("message", timeout=10.0)
                if message.content.lower() == "yes" and message.author in voice_channel.members:
                    if message.author not in polls[ctx.guild.id]["votes"]:
                        polls[ctx.guild.id]["votes"].add(message.author)
                        await play_yes_sound(voice_client)
                        time.sleep(1)
            except asyncio.TimeoutError:
                await ctx.send("Poll timed out.")
                break
        if len(polls[ctx.guild.id]["votes"]) >= (non_excluded_count - 2):
            await ctx.send(f"{username} has been timed out!")
            await member.edit(timed_out_until=utcnow() + timedelta(minutes=.1))
        await voice_client.disconnect()
        del polls[ctx.guild.id]
    else:
        await ctx.send("You must be in a voice channel and have more than two people in the channel to initiate the vote.")

async def play_yes_sound(voice_client):
    audio_source = discord.FFmpegPCMAudio('sound.mp3')
    if not voice_client.is_playing():
        voice_client.play(audio_source)

bot.run(token)