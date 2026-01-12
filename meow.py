import asyncio
import os

from discord.ext import commands
from discord.ext.commands import Context

import config
from SECRETS import DISCORD_TOKEN
import discord
from helper_functions import parsetime
from datetime import datetime
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)


@bot.event
async def on_ready():
    await bot.get_channel(config.TESTING_CHANNEL).send("bot ready!")
@bot.command(aliases=['datedbacklog'])
async def dated_backlog(ctx: discord.ext.commands.Context, time_length: str, channel_id: int):
    end_time_seconds = datetime.now().timestamp() - parsetime(time_length)
    total_added = 0
    channel: discord.TextChannel = ctx.guild.get_channel(channel_id)
    await ctx.reply(f"saving data points in <#{channel.id}> from <t:{int(end_time_seconds)}:R>")
    file_path = f'data/{time_length}.{channel.name}.txt'
    try:
        os.remove(file_path)
    except FileNotFoundError as e:
        print(f"File not found, ignoring! :: {e}, ")
    async for message in channel.history(limit=None):
        if message.created_at.timestamp() < end_time_seconds:
            break
        total_added += 1
        with open(file_path, 'a', encoding='utf-8', errors='replace') as file:
            file.write(f"{message.content}\n")
        print(f"{total_added} ADDED: {message.content}")
    if channel_id in [config.PLAYER_SAVE_CHANNEL]:
        await ctx.reply(f"Done! found {total_added} data points inside of {channel.name} (hidden because im evil pranked)",)
        return
    await ctx.reply(f"Done! found {total_added} data points inside of <#{channel.id}>", file=discord.File(file_path))

@bot.event
async def on_command_error(ctx: Context, error: Exception) -> None:
    if isinstance(error, discord.ext.commands.CheckFailure):
        await ctx.message.add_reaction("❌")
    elif isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.message.add_reaction("❔")
    else:
        await ctx.reply(f"Error occurred! {error}")

bot.run(DISCORD_TOKEN)


