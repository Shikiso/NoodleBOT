import discord
from discord.ext import commands

class server_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        for guild in self.bot.guilds:
            for member in guild.members:
                print(member)

async def setup(bot):
    await bot.add_cog(server_cog(bot))