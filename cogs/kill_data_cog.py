import discord
from discord.ext import commands
from discord.ext.commands import Context

import config
from helper_functions import get_last_message, set_last_message


class kill_data_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def kbacklog(self, ctx: Context):
        total_added = 0
        channel: discord.TextChannel = self.bot.get_channel(config.KILLS_CHANNEL)
        this_last_seen = get_last_message(config.KILLS_CHANNEL)
        await ctx.reply("okay! look in console for processing info")
        async for message in channel.history(limit=None):
            if message.id == this_last_seen:
                break
            if total_added == 0:
                new_last_seen = message.id
            total_added += 1
            data_version = message.content.split(" ")[0].removesuffix(")").removeprefix("(")
            with open(f'data/{data_version}.kills.txt', 'a') as file:
                file.write(f"{message.content}\n")
            print(f"{total_added} ADDED: {message.content}")
        await ctx.reply(f"Done! found {total_added} new data points")
        set_last_message(config.KILLS_CHANNEL, new_last_seen)


async def setup(bot):
    await bot.add_cog(kill_data_cog(bot))