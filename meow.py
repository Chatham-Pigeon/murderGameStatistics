from discord.ext import commands

from SECRETS import DISCORD_TOKEN
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

def parse_message(message: str):
    split_content = message.split()
    role = split_content.pop(2).removesuffix(":")
    useless = split_content.pop(0)
    useless = split_content.pop(0)
    bought_items = []
    for i in split_content:
        i = i.replace("[", "")
        i = i.replace("]", "")
        i = i.replace(",", "")
        bought_items.append(i)
    return bought_items, role

def parse_map(message: str):


@bot.command()
async def parse(ctx, *, content ):
    bought_items, role = parse_message(content)
    await ctx.reply(f"items: {bought_items}, role: {role}")
@bot.command()
async def mparse(ctx, *, cotent):

@bot.event
async def on_message(message: discord.Message):
    if message.author.id == 1376020183302275264:
        bought_items, role = parse_message(message.content)
        with open('purchases.txt', 'a') as file:
            file.write(f'{role}:{" ".join(bought_items)}\n')
        await message.add_reaction("✅")
    await bot.process_commands(message)

@bot.command()
async def backlog(ctx):
    total_added = 0
    total_not_added = 0
    channel = bot.get_channel(1376020164780363846)
    saw_reaction = False
    async for message in channel.history(limit=None):
        for reaction in message.reactions:
            if reaction.emoji == "✅":
                saw_reaction = True
                break
        if saw_reaction is False or 1 == 1:
            total_added = total_added + 1
            print(f"{total_added} FOUND: {message.content}")
            bought_items, role = parse_message(message.content)
            with open('purchases.txt', 'a') as file:
                file.write(f'{role}:{" ".join(bought_items)}\n')
            #await message.add_reaction("✅")
        else:
            total_not_added = total_not_added + 1
            print(f"{total_not_added} NOT FOUND: {message.content}")

@bot.command()
async def after(ctx, message_id: int):
    time = bot.get_channel(1376020164780363846).get_partial_message(message_id).created_at
    channel = bot.get_channel(1376020164780363846)
    saw_reaction = False
    async for message in channel.history(after=time, limit=None):
        for reaction in message.reactions:
            if reaction.emoji == "✅":
                saw_reaction = True
        if saw_reaction is False:
            print(f"FOUND: {message.content}")
            bought_items, role = parse_message(message.content)
            with open('purchases.txt', 'a') as file:
                file.write(f'{role}:{" ".join(bought_items)}\n')
            await message.add_reaction("✅")
        else:
            print(f"NOT FOUND: {message.content}")


bot.run(DISCORD_TOKEN)


