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

@bot.command()
async def parse(ctx, *, content ):
    bought_items, role = parse_message(content)
    await ctx.reply(f"items: {bought_items}, role: {role}")
@bot.event
async def on_message(message: discord.Message):
    if message.author.id == 1376020183302275264:
        bought_items, role = parse_message(message.content)
        with open('purchases.txt', 'a') as file:
            file.write(f'{role}:{" ".join(bought_items)}\n')
        await message.add_reaction("✅")
    await bot.process_commands(message)


bot.run(DISCORD_TOKEN)