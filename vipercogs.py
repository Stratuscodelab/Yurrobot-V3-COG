import discord
from discord.ext import commands
from config import BOT_TOKEN


intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")
    await bot.load_extension('cogs.links') # Load the yurrogm cog
    await bot.load_extension('cogs.searchrecords') # Load the yurrogm cog
    await bot.load_extension('cogs.yurrogm') # Load the yurrogm cog
    await bot.load_extension('cogs.lookupnft') # Load the yurrogm cog
    await bot.load_extension('cogs.yurrostats') # Load the yurrogm cog
    await bot.load_extension('cogs.allcharacters') # Load the yurrogm cog
    await bot.load_extension('cogs.about') # Load the yurrogm cog
    await bot.load_extension('cogs.comic') # Load the yurrogm cog
    await bot.load_extension('cogs.space') # Load the yurrogm cog
    await bot.load_extension('seen.space') # Load the yurrogm cog







    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")

bot.run(BOT_TOKEN)

