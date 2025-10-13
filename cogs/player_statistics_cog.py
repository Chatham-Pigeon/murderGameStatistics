import discord
from discord.ext import commands
import config
from helper_functions import get_last_message, set_last_message
import json
def parse_statistics_message(message: str):
    # 2025/7/17 10:16PM 22847: {healthHealed: 32.09, map: The Commons, name: maig_1, role: accomplice, alive: true, bowsShot: 20, bowsLanded: 9, damageReceived: 17.845, playersKilled: 1}
    message = message.split(" ")
    message = "".join(message)
    return message


class player_statistics_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sparse(self, ctx, *, content):
        statistic = parse_statistics_message(content)
        await ctx.reply(f"stats {statistic}")

    @commands.command()
    async def sbacklog(self, ctx, add_reaction: bool = False):
        total_added = 0
        channel = self.bot.get_channel(config.PLAYER_STATISTICS_CHANNEL)
        await ctx.reply("okay! look in console for processing info")
        this_last_seen = get_last_message(config.PLAYER_STATISTICS_CHANNEL)
        async for msg in channel.history(limit=None):
            message: discord.Message = msg
            message_content: str = message.content
            total_added = total_added + 1
            if message_content.startswith("("):
                data_version = message_content.split(" ")[0].replace("(", "").replace(")", "")
            else:
                game_version  = "0.0"
                break # data version is 0.0... i dont need to update this data it shouldn't change
            if message.id == this_last_seen:
                break
            if total_added == 0:
                new_last_seen = message.id
            with open(f'data/{data_version}.statistics.txt', 'a') as file:
                file.write(f'{message.content}\n')
            if add_reaction:  # only show if enabled, adding reaction slows code down largely
                await message.add_reaction("✅")
            print(f"{total_added} ADDED: {message.content}")
        # done!
        await ctx.reply(f"Done! found {total_added} new data points")
        set_last_message(config.PLAYER_STATISTICS_CHANNEL, new_last_seen)



    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == config.PURCHASE_STATS_WEBHOOK_ID:
            return
            statistics = parse_statistics_message(message.content)
            with open('data/statistics.txt', 'a') as file:
                #file.write(f'{role}:{" ".join(bought_items)}\n')
                pass
            await message.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(player_statistics_cog(bot))