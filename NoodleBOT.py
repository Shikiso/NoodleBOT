# Invite Link: https://discord.com/api/oauth2/authorize?client_id=1031205330039865384&permissions=8&scope=bot
import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(getenv("TOKEN"))