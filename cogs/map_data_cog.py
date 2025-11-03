import discord
from discord.ext import commands
from datetime import datetime

import config
from helper_functions import get_last_message, set_last_message


def parse_map_message(content: str):
    # (1.0) 2025/5/28 09:53AM 6747: The Aquarium:innocents:true:163:1:0
    data_list = content.split(":")
    data_version = data_list.pop(0).split(" ") #"(1.0) 2025/5/28 09"
    if len(data_version) == 3: # game version exists
        data_version = data_version[0].replace("(", "").replace(")", "")
    else:
        data_version = "0.0"
    data_list.insert(0, data_list.pop(0).split()[1])
    data_list[1] = data_list[1].strip()
    data_list[1] = data_list[1].replace(" ", "_")
    data_list[1] = data_list[1].replace("™", "")
    return data_list, data_version


class map_data_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def mparse(self, ctx, *, content):
        the_list, data_version = parse_map_message(content)
        await ctx.reply(f"{the_list} \n {data_version}")

    @commands.command()
    async def mbacklog(self, ctx, add_reaction: bool = False):
        total_added = 0
        total_not_added = 0
        channel = self.bot.get_channel(config.ROUNDS_STATS_CHANNEL)
        this_last_seen = get_last_message(config.ROUNDS_STATS_CHANNEL)
        await ctx.reply("okay! look in console for processing info")
        async for message in channel.history(limit=None):
            data, game_version = parse_map_message(message.content)
            if game_version == "0.0":
                break
            if message.id == this_last_seen:
                break
            if total_added == 0:
                new_last_seen = message.id
            with open(f'old_data/{game_version}.map_data.txt', 'a') as file:
                file.write(f'{" ".join(data)}\n')
            total_added = total_added + 1
            print(f"{total_added} ADDED: {message.content}")
        await ctx.reply(
            f"Done! found {total_added} new old_data points, found {total_not_added} already added old_data points.")
        set_last_message(config.ROUNDS_STATS_CHANNEL, new_last_seen)


    @commands.command()
    async def mdatedbacklog(self, ctx, add_reaction: bool = False):
        total_added = 0
        total_not_added = 0
        bye = 0
        channel = self.bot.get_channel(config.ROUNDS_STATS_CHANNEL)
        await ctx.reply("okay! look in console for processing info")
        async for message in channel.history(limit=None):
            message: discord.Message = message
            data, game_version = parse_map_message(message.content)
            for reaction in message.reactions:
                if reaction.emoji == "8️⃣":
                    bye = 1
                    break
            if bye == 1:
                break
            with open(f'old_data/lastmonth.map_data.txt', 'a') as file:
                file.write(f'{" ".join(data)}\n')
            total_added = total_added + 1
            print(f"{total_added} ADDED: {message.content}")
        await ctx.reply(f"Done! found {total_added} new old_data points, found {total_not_added} already added old_data points.")


    @commands.command()
    async def mreload(self, ctx):
        self.bot.reload_extension(f'cogs.map_data_cog')
        await ctx.send(f'Reloaded map old_data ')
    @commands.Cog.listener()
    async def on_message(self, message = discord.Message):
        if message.author.id == config.ROUNDS_STATS_WEBHOOK_ID:
            return
            data = parse_map_message(message.content)
            with open('old_data/map_data.txt', 'a') as file:
                file.write(f'{" ".join(data)}\n')
            await message.add_reaction("✅")



async def setup(bot):
    await bot.add_cog(map_data_cog(bot))