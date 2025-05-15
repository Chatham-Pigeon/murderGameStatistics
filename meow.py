from enum import pickle_by_global_name

from discord import Spotify
from discord.ext import commands

from SECRETS import DISCORD_TOKEN
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

DEBUG_CHANNEL = 1372243695268663306
LISTENING_CHANNEL = 1372243695268663306
PIGEON_ID = 272534243899342849
@bot.event
async def on_ready():
    pass
@bot.command()
async def stalk(ctx: discord.ext.commands.Context, userid: int = None):
    if userid is None:
        userid = ctx.author.id
    user: discord.Member = bot.get_guild(ctx.guild.id).get_member(userid)


    for activity in user.activities:
        if isinstance(activity, discord.Spotify):
            await ctx.reply(activity.title)

@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member):
    if after.id == PIGEON_ID:
        return 
    was_listening = False
    for activity in before.activities:
        if isinstance(activity, Spotify):
            was_listening =  True
    for activity in after.activities:
        if isinstance(activity, Spotify):
            if was_listening is True:
                await bot.get_channel(LISTENING_CHANNEL).send(f'`{after.name}` is listening to "{activity.title}"')
            else:
                await bot.get_channel(LISTENING_CHANNEL).send(f'<@{PIGEON_ID}>`{after.name}` STARTED listening to "{activity.title}"')



bot.run(DISCORD_TOKEN)