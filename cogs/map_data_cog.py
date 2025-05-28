from discord.ext import commands


class map_data_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def test(self, ctx):
        pass