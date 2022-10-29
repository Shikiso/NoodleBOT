# Invite Link: https://discord.com/api/oauth2/authorize?client_id=1031205330039865384&permissions=8&scope=bot
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from os import getenv, listdir
from bin.Embed_Handler import embed
from bin.variables import db, Users
from User.User import User
#import bin.setup # sets up database and other functionality

intents_varaible = discord.Intents.all()
noodle_server = discord.Object(id=992294737405026324)

class aclient(discord.Client):

    def __init__(self):
        super().__init__(intents=intents_variable)
        self.synced = False
        self.Check_Server_Members = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=noodle_server)
            self.synced = True
        
        if not self.Check_Server_Members:
            self.create_user_objects()
        print("[+] NoodleBOT is ready!")
    
    def create_user_objects(self):
        print("[+] Creating user objects...")
        if not self.Check_Server_Members:
            for guild in self.guilds:
                for member in guild.members:
                    if not member.bot:
                        id = member.id
                        if not db.get_user_info(id):
                            userObj = User(id, 0, '', '', '', '')
                            userInfo = userObj.user_info
                            db.add_user_to_database(userInfo)
                        else:
                            data = db.get_user_info(id)
                            userObj = User(data[0], data[1], data[2], data[3], data[4], data[5])
                        Users[id] = userObj
            self.Check_Server_Members = True

client = aclient()
tree = app_commands.CommandTree(client)
load_dotenv()

# Commands
@tree.command(name="inventory", description="Shows your user inventory.", guild=noodle_server)
async def self(interaction: discord.Integration):
    print(interaction.user.id)
    
    # e = embed(title="Title1", description="Description").get_embed()

    # await interaction.response.send_message(embed=e)

@tree.command(name="buy", description="Buy item", guild=noodle_server)
async def self(interaction: discord.Integration, item: str, amount: int):
    user_id = interaction.user.id
    if user_id not in Users:
        client.create_user_objects()

    userObj = Users[user_id]
    itemObj = db.get_item_by_name(item)
    if not itemObj:
        e = embed(title="Buying Item", description=f"{item} does not exist!").get_embed()

    user_money = userObj.Money
    item_price = itemObj[2]

    if user_money >= item_price:
        user_money = userObj.sub_money(item_price)
        userObj.add_item(itemObj[0])
    

    await interaction.response.send_message(embed=e)

client.run(getenv("TOKEN"))