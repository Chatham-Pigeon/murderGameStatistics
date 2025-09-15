import discord
from discord.ext import commands
from discord.ext.commands import Context

import config

class map_voting_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vbacklog(self, ctx: Context,):
        channel: discord.TextChannel = self.bot.get_channel(config.VOTING_STATS_CHANNEL)
        await ctx.reply("okay! look in console for processing info")
        total_added = 0
        async for message in channel.history(limit=None):
            total_added += 1
            data_version = message.content.split(" ")[0].replace("(", "").replace(")", "")
            # (1.0) 2025/9/15 06:49PM plot: Behind the Waterfall,0:Tropics,3:The Brigade,0:Temple of RAA Jr.,0:Fiend Casino,0:random:0#13
            with open(f'data/{data_version}.voting_data.txt', 'a') as file:
                file.write(f'{message.content}\n')
            print(f"{total_added} ADDED: {message.content}")


async def setup(bot):
    await bot.add_cog(map_voting_cog(bot))