import discord
from discord.ext import commands
from discord.ext.commands import Context

import config
from helper_functions import get_last_message, set_last_message

class map_voting_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vbacklog(self, ctx: Context,):
        channel: discord.TextChannel = self.bot.get_channel(config.VOTING_STATS_CHANNEL)
        this_last_seen = get_last_message(config.VOTING_STATS_CHANNEL)
        await ctx.reply("okay! look in console for processing info")
        total_added = 0
        async for message in channel.history(limit=None):
            if message.id == this_last_seen:
                break
            if total_added == 0:
                new_last_seen = message.id
            total_added += 1
            data_version = message.content.split(" ")[0].replace("(", "").replace(")", "")
            # (1.0) 2025/9/15 06:49PM plot: Behind the Waterfall,0:Tropics,3:The Brigade,0:Temple of RAA Jr.,0:Fiend Casino,0:random:0#13
            with open(f'data/{data_version}.voting_data.txt', 'a') as file:
                file.write(f'{message.content}\n')
            print(f"{total_added} ADDED: {message.content}")
        set_last_message(config.VOTING_STATS_CHANNEL, new_last_seen)
        await ctx.reply(f"DONE! found {total_added} new data points")

async def setup(bot):
    await bot.add_cog(map_voting_cog(bot))