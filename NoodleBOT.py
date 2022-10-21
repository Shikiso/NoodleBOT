# Invite Link: https://discord.com/api/oauth2/authorize?client_id=1031205330039865384&permissions=8&scope=bot
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv, listdir
import bin.setup # sets up database and other functionality

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

@bot.event
async def on_ready():
    print("[+] NoodleBOT is ready!")
    for cog in listdir("./cogs"):
        if cog.endswith(".py"):
            try:
                await bot.load_extension("cogs." + cog[:-3])
                print(cog + " was loaded")
            except Exception as e:
                print("Cog loading Error:", e)

bot.run(getenv("TOKEN"))