import discord
from discord.ext import commands
from Local_Vars.variables import db
from User.User import User

class server_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Check_Server_Members = False

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not self.Check_Server_Members:
            for guild in self.bot.guilds:
                for member in guild.members:
                    if not member.bot:
                        id = member.id
                        
                        if not db.user_exists_in_database(id):
                            userObj = User(id, 0, '', '', '', '')
                            userInfo = userObj.user_info
                            db.add_user_to_database(userInfo)
            self.Check_Server_Members = True

async def setup(bot):
    await bot.add_cog(server_cog(bot))