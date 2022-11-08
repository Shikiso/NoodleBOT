# Invite Link: https://discord.com/api/oauth2/authorize?client_id=1031205330039865384&permissions=8&scope=bot
import bin.config # sets up database and other functionality
from bin.needed_vars import *
from bin.quick_access import Users, Items, Items_IDs, update_item_amount_existing
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
ItemHandler = bin.config.ItemHandler()
TransactionCounter = 1

# Functions to help with commands
def get_user_object(user_id):
    userObj = Users[user_id]
    return userObj

def pass_transaction(itemID=None):
    global TransactionCounter
    log.debug(f"[TRANSACTION] Transaction made {TransactionCounter} in total.")
    if TransactionCounter >= 50 and itemID:
        ItemHandler.update_price_to_demand(itemID)

    TransactionCounter += 1

# Admin Commands
@tree.command(name="donate", description="Gives users money.")
async def self(interaction: discord.Integration, user: discord.Member, amount: int):
    user_id = interaction.user.id
    if user_id in NoodleBOT_ADMINS:
        recieving_user_id = user.id
        
        userObj = get_user_object(recieving_user_id)
        userObj.add_money(amount)
        log.warning(f"[ADMIN] {user_id} : {interaction.user.name}, donated {recieving_user_id} : {user.name}, ${amount}")
        e = embed(title="ADMIN COMMAND", description=f"Donated ${amount} to {user}").get_embed()
        await interaction.response.send_message(embed=e)

@tree.command(name="create", description="Creates a new item.")
async def self(interaction: discord.Integration, name: str, exists: int):
    ItemHandler.create_item(name, exists)
    ItemHandler.save_item_to_database(name, exists)
    with open("./Items/items.txt", 'a') as f:
        f.write(name + ',' + str(exists) + '\n')
    e = embed(title="ADMIN COMMAND", description=f"Created {name} item with {exists} existing").get_embed()
    await interaction.response.send_message(embed=e)

# Commands
@tree.command(name="inventory", description="Shows your user inventory.")
async def self(interaction: discord.Integration, member: discord.Member = None):
    if member is None:
        user = interaction.user
    else:
        user = member
    userObj = Users[user.id]
    userItems = userObj.Items

    if userItems != {}:
        fields_list = []
        for item, amount in userItems.items():
            itemName = Items[item][0]
            fields_list.append((itemName, str(amount), False))

        e = embed(title="Inventory", fields=fields_list).get_embed()
    else:
        e = embed(title="Inventory", description=f"You own no items").get_embed()
    
    await interaction.response.send_message(embed=e)


@tree.command(name="buy", description="Buy item")
async def self(interaction: discord.Integration, item: str, amount: int = 1):
    user = interaction.user
    userObj = Users[user.id]
    userMoney = userObj.Money

    if item not in Items_IDs:
        e = embed(title="Buying Item", description=f"{item} does not exist!").get_embed()
    else:
        itemID = Items_IDs[item]
        itemInfo = Items[itemID]
        itemPrice = itemInfo[1]

        if Items[itemID][2] == 0 or Items[itemID][2] < amount:
            e = embed(title="Buying Item", description=f"No more or not enough {item} are being sold in shop").get_embed()
        else:
            moneyOwed = itemPrice * amount
            if userMoney >= moneyOwed:
                for _ in range(amount):
                    userObj.add_item(itemID)
                userObj.sub_money(moneyOwed)
                e = embed(title="Buying Item", description=f"Bought {amount} {item}").get_embed()
                Items[itemID][2] -= amount
                update_item_amount_existing(itemID, Items[itemID][2])
                pass_transaction(itemID)
            else:
                e = embed(title="Buying Item", description=f"Not enough money for {amount} {item}").get_embed()

    await interaction.response.send_message(embed=e)

@tree.command(name="sell", description="Sell item")
async def self(interaction: discord.Integration, item: str, amount: int = 1):
    user = interaction.user
    userObj = Users[user.id]
    userItems = userObj.Items

    if item not in Items_IDs:
        e = embed(title="Selling Item", description=f"{item} does not exist!").get_embed()
    else:
        itemID = Items_IDs[item]
        itemInfo = Items[itemID]
        itemPrice = itemInfo[1]

        if itemID in userItems:
            amountOwned = userItems[itemID]

            if amount <= amountOwned:
                for _ in range(amount):
                    userObj.sub_item(itemID)
                moneyOwed = itemPrice * amount
                userObj.add_money(moneyOwed)
                Items[itemID][2] += amount
                update_item_amount_existing(itemID, Items[itemID][2])
                pass_transaction(itemID)
                e = embed(title="Selling Item", description=f"Sold {amount} {item} for ${moneyOwed}").get_embed()
            else:
                e = embed(title="Selling Item", description=f"You do not own {amount} {item}").get_embed()
        else:
            e = embed(title="Selling Item", description=f"You do not own {item}").get_embed()
    
    await interaction.response.send_message(embed=e)

@tree.command(name="balance", description="Check users balance")
async def self(interaction: discord.Integration, member: discord.Member = None):
    if member is None:
        user = interaction.user
    else:
        user = member
    userObj = Users[user.id]
    e = embed(title="Balance", description=f"{user} has ${userObj.Money}").get_embed()
    await interaction.response.send_message(embed=e)

if __name__ == "__main__":
    client.run(getenv("TOKEN"))