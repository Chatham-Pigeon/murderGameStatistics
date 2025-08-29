import asyncio

from discord.ext import commands

import config
from SECRETS import DISCORD_TOKEN
import discord

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

@bot.event
async def on_ready():
    await bot.get_channel(config.TESTING_CHANNEL).send("bot ready!")

initial_extensions = ['cogs.purchase_data_cog', 'cogs.map_data_cog', 'cogs.player_statistics_cog']
async def main():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f"{extension} loaded successfully.")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

asyncio.run(main())
bot.run(DISCORD_TOKEN)


