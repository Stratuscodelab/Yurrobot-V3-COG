import discord
import io
from discord.ext import commands
from PIL import Image
import sqlite3
import random
import json
from discord import app_commands
import asyncio

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)


connection = sqlite3.connect('viperdevmac.db')
c = connection.cursor()


class allcharacters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @bot.tree.command(name="allcharacters", description="View all characters records in SpaceAddicts and Rontacklebox collection")
    async def allcharacters(self, interaction):
        # Execute a SELECT statement to retrieve all names from the database
        c.execute("SELECT name, 'Space Addicts' as source FROM spaceaddicts UNION SELECT name, 'Ron Tacklebox' as source FROM ront UNION SELECT name, 'Shop' as source FROM shop")
        results = c.fetchall()

        # If results are found, create a list of names and send it to the user via an ephemeral message in the channel
        if results:
            # Format the results into a dictionary, where the key is the source and the value is a list of names from that source
            formatted_results = {}
            for name, source in results:
                if source not in formatted_results:
                    formatted_results[source] = []
                formatted_results[source].append(name)

            # Create a message with the formatted results
            message = ''
            for source, names in formatted_results.items():
                message += f'\n{source.upper()}:\n' + '\n'.join(names) + '\n'

            # Split the message into chunks of 2000 characters and send each chunk as an ephemeral message
            chunks = [message[i:i+2000] for i in range(0, len(message), 2000)]
            for chunk in chunks:
                embed = discord.Embed(title='Names in Databases', description=chunk, color=0x00ff00)
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            # If no results are found, send a message in the channel indicating that there are no names in the databases
            embed = discord.Embed(title='Names in Databases', description='There are no names in the databases.', color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)

            
            

async def setup(bot):
    await bot.add_cog(allcharacters(bot))

