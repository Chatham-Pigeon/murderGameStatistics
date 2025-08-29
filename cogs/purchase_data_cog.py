from os.path import split

import discord
from discord.ext import commands
from discord.ext.commands import Context

import config

def parse_purchase_message(message: str):
    # original message formatted in (1.0) YEAR/MM/DD HH:MMA/PM ROLE: [item, item, item]
    split_content = message.split()
    if message.startswith("("):
        data_version = split_content.pop(0).replace("(", "").replace(")", "")
    else:
        data_version = "0.0"
    role = split_content.pop(2).removesuffix(":")  # parse the role from the original message and remove it
    split_content.pop(0)  # remove the YEAR/MM/DD
    split_content.pop(0)  # remove the HH:mmA/PM
    bought_items = []
    for i in split_content:  # loop through remaining content in the message (just items)
        # remove unnecessary punctuation
        i = i.replace("[", "")
        i = i.replace("]", "")
        i = i.replace(",", "")
        bought_items.append(i)
    return bought_items, role, data_version


class purchase_data_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pparse(self, ctx, *, content):
        bought_items, role, data_version = parse_purchase_message(content)
        await ctx.reply(f"items: {bought_items}, role: {role}, version: {data_version}")

    @commands.command()
    async def pbacklog(self, ctx: Context, add_reaction: bool = False):
        total_added = 0
        total_not_added = 0
        channel: discord.TextChannel = self.bot.get_channel(config.PURCHASE_STATS_CHANNEL)
        saw_reaction = False
        await ctx.reply("okay! look in console for processing info")
        async for message in channel.history(limit=None):
            if message.id == 1395379386051596339:
                break
            for reaction in message.reactions:
                if reaction.emoji == "✅":
                    saw_reaction = True
                    break
            if saw_reaction is False or 1 == 1:
                total_added = total_added + 1
                bought_items, role, data_version = parse_purchase_message(message.content)
                with open(f'data/{data_version}.purchases.txt', 'a') as file:
                    file.write(f'{role}:{" ".join(bought_items)}\n')
                if add_reaction:  # only show if enabled, adding reaction slows code down largely
                    await message.add_reaction("✅")
                print(f"{total_added} ADDED: {message.content}")
            else:
                total_not_added = total_not_added + 1
                print(f"{total_not_added} NOT ADDED: {message.content}")
        await ctx.reply(
            f"Done! found {total_added} new data points, found {total_not_added} already added data points.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == config.PURCHASE_STATS_WEBHOOK_ID:
            bought_items, role = parse_purchase_message(message.content)
            with open('data/purchases.txt', 'a') as file:
                file.write(f'{role}:{" ".join(bought_items)}\n')
            await message.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(purchase_data_cog(bot))