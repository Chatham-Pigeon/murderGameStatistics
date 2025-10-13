from os.path import split

import discord
from discord.ext import commands
from discord.ext.commands import Context

import config
from helper_functions import get_last_message, set_last_message


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
        channel: discord.TextChannel = self.bot.get_channel(config.PURCHASE_STATS_CHANNEL)
        this_last_seen = get_last_message(config.PURCHASE_STATS_CHANNEL)
        await ctx.reply("okay! look in console for processing info")
        async for message in channel.history(limit=None):
            if message.id == this_last_seen:
                break
            if total_added == 0:
                new_last_seen = message.id
            total_added += 1
            bought_items, role, data_version = parse_purchase_message(message.content)
            if data_version == "0.0":
                break
            with open(f'data/{data_version}.purchases.txt', 'a') as file:
                file.write(f'{role}:{" ".join(bought_items)}\n')
            print(f"{total_added} ADDED: {message.content}")
        await ctx.reply(f"Done! found {total_added} new data points")
        set_last_message(config.PURCHASE_STATS_CHANNEL, new_last_seen)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == config.PURCHASE_STATS_WEBHOOK_ID:
            return
            bought_items, role = parse_purchase_message(message.content)
            with open('data/purchases.txt', 'a') as file:
                file.write(f'{role}:{" ".join(bought_items)}\n')
            await message.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(purchase_data_cog(bot))