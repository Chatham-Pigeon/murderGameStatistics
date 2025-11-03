import asyncio
from encodings.aliases import aliases

from discord.ext import commands

import config
from SECRETS import DISCORD_TOKEN
import discord
from helper_functions import parsetime, get_last_message, set_last_message
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
    async for message in channel.history(limit=None):
        if message.created_at.timestamp() < end_time_seconds:
            break
        total_added += 1
        with open(f'new_data/{time_length}.{channel.name}.txt', 'a') as file:
            file.write(f"{message.content}\n")
        print(f"{total_added} ADDED: {message.content}")
    await ctx.reply(f"Done! found {total_added} data points inside of <#{channel.id}>")

@bot.command(aliases=['catchup'])
async def catch_up(ctx: discord.ext.commands.Context, channel_id: int = None):
    if channel_id is None:
        data_category: discord.CategoryChannel = discord.utils.get(ctx.guild.categories, id=config.DATA_CATEGORY_ID)
        channels_list = data_category.channels
    else:
        channels_list = [ctx.guild.get_channel(channel_id)]
    for channel in channels_list:
        total_added = 0
        this_last_seen = get_last_message(channel.id)
        await ctx.reply(f"Saving ALL data points for <#{channel.id}>")
        async for message in channel.history(limit=None):
            if message.id == this_last_seen:
                break
            if total_added == 0:
                new_last_seen = message.id
            total_added += 1
            with open(f'new_data/allTime.{channel.name}.txt', 'a', encoding='utf-8', errors='replace') as file:
                file.write(f'{int(message.created_at.timestamp())}#{message.content}\n')
            print(f"{total_added} ADDED: {message.content}")
        # done!
        await ctx.reply(f"saved {total_added} data points from <#{channel.id}>")
        set_last_message(channel.id, new_last_seen)


initial_extensions = ['cogs.purchase_data_cog', 'cogs.map_data_cog', 'cogs.player_statistics_cog', 'cogs.map_voting_cog', 'cogs.player_data_cog', 'cogs.evil_data', 'cogs.kill_data_cog']
async def main():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"{extension} loaded successfully.")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

asyncio.run(main())
bot.run(DISCORD_TOKEN)


