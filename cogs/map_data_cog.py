import discord
from discord.ext import commands

import config

def parse_map_message(content: str):
    # 2025/5/28 09:53AM 6747: The Aquarium:innocents:true:163:1:0
    data_list = content.split(":")
    data_list.pop(0)
    data_list.insert(0, data_list.pop(0).split()[1])
    data_list[1] = data_list[1].strip()
    data_list[1] = data_list[1].replace(" ", "_")
    data_list[1] = data_list[1].replace("™", "")
    return data_list


class map_data_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def mparse(self, ctx, *, content):
        the_list = parse_map_message(content)
        await ctx.reply(the_list)

    @commands.command()
    async def mbacklog(self, ctx, add_reaction: bool = False):
        total_added = 0
        total_not_added = 0
        channel = self.bot.get_channel(config.ROUNDS_STATS_CHANNEL)
        saw_reaction = False
        await ctx.reply("okay! look in console for processing info")
        async for message in channel.history(limit=None):
            for reaction in message.reactions:
                if reaction.emoji == "✅":
                    saw_reaction = True
                    break
            if saw_reaction is False or 1 == 1:
                total_added = total_added + 1
                data = parse_map_message(message.content)
                with open('map_data.txt', 'a') as file:
                    file.write(f'{" ".join(data)}\n')
                if add_reaction:  # only show if enabled, adding reaction slows code down largely
                    await message.add_reaction("✅")
                print(f"{total_added} ADDED: {message.content}")
            else:
                total_not_added = total_not_added + 1
                print(f"{total_not_added} NOT ADDED: {message.content}")
        await ctx.reply(
            f"Done! found {total_added} new data points, found {total_not_added} already added data points.")

    @commands.command()
    async def mreload(self, ctx):
        self.bot.reload_extension(f'cogs.map_data_cog')
        await ctx.send(f'Reloaded map data ')
    @commands.Cog.listener()
    async def on_message(self, message = discord.Message):
        if message.author.id == config.ROUNDS_STATS_WEBHOOK_ID:
            data = parse_map_message(message.content)
            with open('map_data.txt', 'a') as file:
                file.write(f'{" ".join(data)}\n')
            await message.add_reaction("✅")



async def setup(bot):
    await bot.add_cog(map_data_cog(bot))