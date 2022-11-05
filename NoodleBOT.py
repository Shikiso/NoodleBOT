# Invite Link: https://discord.com/api/oauth2/authorize?client_id=1031205330039865384&permissions=8&scope=bot
import bin.config # sets up database and other functionality
from bin.needed_vars import *
from bin.quick_access import Users
from bin.Embed_Handler import embed
from Members.load_members import start

import discord
from discord import app_commands
from dotenv import load_dotenv
from os import getenv

intents_varaible = discord.Intents.all()
noodle_server = discord.Object(id=992294737405026324)

class aclient(discord.Client):

    def __init__(self):
        super().__init__(intents=intents_varaible)
        self.synced = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=noodle_server)
            self.synced = True

        start(self)
        log.info("[+] NoodleBOT is ready!")
    

load_dotenv()
client = aclient()
tree = app_commands.CommandTree(client)
NoodleBOT_ADMINS = [964887596754944100, 1035925157065277550]

# Functions to help with commands
def get_user_object(user_id):
    if user_id not in Users:
        client.create_user_objects()

    userObj = Users[user_id]
    return userObj

# Admin Commands
@tree.command(name="donate", description="Gives users money.", guild=noodle_server)
async def self(interaction: discord.Integration, user: discord.Member, amount: int):
    user_id = interaction.user.id
    if user_id in NoodleBOT_ADMINS:
        recieving_user_id = user.id
    
        if recieving_user_id not in Users:
            client.create_user_objects()
        
        userObj = get_user_object(user_id)
        userObj.add_money(amount)
        log.warning(f"[ADMIN] {user_id} : {interaction.user.name}, donated {user_id} : {user.name}, ${amount}")
        e = embed(title="ADMIN COMMAND", description=f"Donated ${amount} to {user}").get_embed()
        await interaction.response.send_message(embed=e)

# Commands
@tree.command(name="inventory", description="Shows your user inventory.", guild=noodle_server)
async def self(interaction: discord.Integration):
    print(interaction.user.id)
    
    # e = embed(title="Title1", description="Description").get_embed()

    # await interaction.response.send_message(embed=e)

buy_counter = 0
@tree.command(name="buy", description="Buy item", guild=noodle_server)
async def self(interaction: discord.Integration, item: str, amount: int):
    global buy_counter

    user_id = interaction.user.id

    userObj = get_user_object(user_id)
    itemObj = db.get_item(name=item)
    if not itemObj:
        e = embed(title="Buying Item", description=f"{item} does not exist!").get_embed()
    else:
        user_money = userObj.Money
        item_price = itemObj[2]

        if user_money >= item_price:
            user_money = userObj.sub_money(item_price)
            userObj.add_item(itemObj[1])
            e = embed(title="Buying Item", description=f"Bought {item}").get_embed()
        else:
            e = embed(title="Buying Item", description=f"Not enough money for {item}").get_embed()

    await interaction.response.send_message(embed=e)
    buy_counter += 1

    if buy_counter == 2:
        alter_item_price_based_on_demand(itemObj[0])
        buy_counter = 0

client.run(getenv("TOKEN"))