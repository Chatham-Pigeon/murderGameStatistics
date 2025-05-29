import discord
from discord.ext import commands
import config

def parse_purchase_message(message: str):
    # original message formatted in YEAR/MM/DD HH:MMA/PM ROLE: [item, item, item]
    split_content = message.split()
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
    return bought_items, role


class purchase_data_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pparse(self, ctx, *, content):
        bought_items, role = parse_purchase_message(content)
        await ctx.reply(f"items: {bought_items}, role: {role}")

    @commands.command()
    async def pbacklog(self, ctx, add_reaction: bool = False):
        total_added = 0
        total_not_added = 0
        channel = self.bot.get_channel(config.PURCHASE_STATS_CHANNEL)
        saw_reaction = False
        await ctx.reply("okay! look in console for processing info")
        async for message in channel.history(limit=None):
            for reaction in message.reactions:
                if reaction.emoji == "✅":
                    saw_reaction = True
                    break
            if saw_reaction is False or 1 == 1:
                total_added = total_added + 1
                bought_items, role = parse_purchase_message(message.content)
                with open('purchases.txt', 'a') as file:
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
            with open('purchases.txt', 'a') as file:
                file.write(f'{role}:{" ".join(bought_items)}\n')
            await message.add_reaction("✅")

async def setup(bot):
    await bot.add_cog(purchase_data_cog(bot))