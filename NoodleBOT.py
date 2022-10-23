# Invite Link: https://discord.com/api/oauth2/authorize?client_id=1031205330039865384&permissions=8&scope=bot
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from os import getenv, listdir
from bin.Embed_Handler import embed
import bin.setup # sets up database and other functionality

intents_varaible = discord.Intents.default()
noodle_server = discord.Object(id=992294737405026324)

class aclient(discord.Client):

    def __init__(self):
        super().__init__(intents=intents_varaible)
        self.synced = False
        self.loaded_cogs = False
    
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=noodle_server)
            self.synced = True
        
        if not self.loaded_cogs:
            for cog in listdir("./cogs"):
                if cog.endswith(".py"):
                    try:
                        await commands.Bot(command_prefix=None, intents=intents_varaible).load_extension("cogs." + cog[:-3])
                        print("[+] " + cog + " was loaded")
                    except Exception as e:
                        print("[-] Cog loading Error:", e)
            self.loaded_cogs = True
        print("[+] NoodleBOT is ready!")

client = aclient()
tree = app_commands.CommandTree(client)
load_dotenv()

# Commands
@tree.command(name="inventory", description="Shows your user inventory.", guild=noodle_server)
async def self(interaction: discord.Integration):
    e = embed(title="Title1", description="Description").get_embed()

    await interaction.response.send_message(embed=e)

client.run(getenv("TOKEN"))