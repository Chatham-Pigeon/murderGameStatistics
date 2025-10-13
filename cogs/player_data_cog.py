import discord
from discord.ext import commands
from discord.ext.commands import Context

import config

class player_data_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dbacklog(self, ctx: Context,):
        channel: discord.TextChannel = self.bot.get_channel(config.PLAYER_DATA_CHANNEL)
        await ctx.reply("okay! look in console for processing info")
        total_added = 0
        async for message in channel.history(limit=None):
            total_added += 1
            data_version = message.content.split(" ")[0].replace("(", "").replace(")", "")
            with open(f'data/{data_version}.player_data.txt', 'a') as file:
                file.write(f'{message.content}\n')
            print(f"{total_added} ADDED: {message.content}")


async def setup(bot):
    await bot.add_cog(player_data_cog(bot))