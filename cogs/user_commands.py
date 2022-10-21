import discord
from discord.ext import commands
from bin.variables import db
from User.User import User

class user_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def on_message(self, ctx):
        pass

async def setup(bot):
    await bot.add_cog(user_commands(bot))