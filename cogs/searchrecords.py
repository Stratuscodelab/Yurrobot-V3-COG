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


class searchrecords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.tree.command(name="searchrecords", description="Lookup any SpaceAddict by name",)
   # @app_commands.describe(name_of_subject =  "What name should i look up ?")
    async def searchrecords(self, interaction: discord.Interaction, name_of_spaceaddict: str = None, name_of_rontacklebox: str = None, select_this_and_type_random: str = None):
        if select_this_and_type_random is not None and select_this_and_type_random.lower() == "random":
            # Check if either table has records
            c.execute("SELECT COUNT(*) FROM spaceaddicts")
            spaceaddicts_count = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM ront")
            ront_count = c.fetchone()[0]

            if spaceaddicts_count == 0 and ront_count == 0:
                await interaction.response.send_message("No records found in the database.")
                return

            # Select a random table
            table = random.choice(["spaceaddicts", "ront"])

            if table == "spaceaddicts":
                c.execute("SELECT * FROM spaceaddicts")
            else:
                c.execute("SELECT * FROM ront")

            all_results = c.fetchall()

            if all_results:
                random_result = random.choice(all_results)
                # Get the image from the local file system
                image_path = random_result[3]
                with open(image_path, 'rb') as f:
                    image_file = discord.File(f)

                # Create the embed
                embed = discord.Embed(
                    title=random_result[0],
                    description=random_result[2],
                    color=discord.Color.teal()
                )
                with Image.open(image_path) as img:
                    img.thumbnail((300, 300))
                    with io.BytesIO() as output:
                        img.save(output, format="JPEG")
                        image_data = output.getvalue()
                embed.set_image(url="attachment://thumbnail.png")
                embed.set_thumbnail(url="attachment://logoclear.png")
                embed.add_field(name="Title", value=random_result[1], inline=False)
                embed.set_footer(text="Learn more here: Spaceaddicts.io")

                # Send the message and the image files to the user
                await interaction.response.send_message(
                    embed=embed,
                    files=[
                        discord.File(io.BytesIO(image_data), filename='thumbnail.png'),
                        discord.File("logoclear.png", filename='logoclear.png')
                    ]
                )
            else:
                await interaction.response.send_message(f"No records found in the '{table}' table.")
            return

        if name_of_rontacklebox is not None:
            name = name_of_rontacklebox.lower()
            c.execute("SELECT * FROM ront WHERE LOWER(name) = ?", (name,))
            exact_result = c.fetchone()

            # If an exact result is found in ront table, send it to the user
            if exact_result:
                # Get the image from the local file system
                image_path = exact_result[3]
                with open(image_path, 'rb') as f:
                    image_file = discord.File(f)

                # Create the embed
                embed = discord.Embed(
                    title=exact_result[0],
                    description=exact_result[2],
                    color=discord.Color.teal()
                )
                with Image.open(image_path) as img:
                    img.thumbnail((300, 300))
                    with io.BytesIO() as output:
                        img.save(output, format="JPEG")
                        image_data = output.getvalue()
                embed.set_image(url="attachment://thumbnail.png")
                embed.set_thumbnail(url="attachment://logoclear.png")
                embed.add_field(name="Title", value=exact_result[1], inline=False)
                embed.set_footer(text="Learn more here: Spaceaddicts.io")
                
            if name_of_rontacklebox is not None:
                name = name_of_rontacklebox.lower()
                c.execute("SELECT * FROM ront WHERE LOWER(name) = ?", (name,))
                exact_result = c.fetchone()

                # If an exact result is found in ront table, send it to the user
                if exact_result:
                    # Get the image from the local file system
                    image_path = exact_result[3]
                    with open(image_path, 'rb') as f:
                        image_file = discord.File(f)

                    # Create the embed
                    embed = discord.Embed(
                        title=exact_result[0],
                        description=exact_result[2],
                        color=discord.Color.teal()
                    )
                    with Image.open(image_path) as img:
                        img.thumbnail((300, 300))
                        with io.BytesIO() as output:
                            img.save(output, format="JPEG")
                            image_data = output.getvalue()
                    embed.set_image(url="attachment://thumbnail.png")
                    embed.set_thumbnail(url="attachment://logoclear.png")
                    embed.add_field(name="Title", value=exact_result[1], inline=False)
                    embed.set_footer(text="Learn more here: Spaceaddicts.io")

                    # Send the message and the image files to the user
                    await interaction.response.send_message(
                        embed=embed,
                        files=[
                            discord.File(io.BytesIO(image_data), filename='thumbnail.png'),
                            discord.File("logoclear.png", filename='logoclear.png')
                        ]
                    )
                else:
            # Execute a SELECT statement using LIKE to search for similar items
                    c.execute("SELECT * FROM ront WHERE LOWER(name) LIKE ?", (f'%{name}%',))
                    results = c.fetchall()
                    # If multiple results are found, suggest them to the user
                    if results:
                        message_content = "Multiple items found..."
                        for r in results:
                            message_content += f"\n- {r[0]} ({r[1]})"
                        message_content += "\nPlease refine your search."
                        await interaction.response.send_message(message_content)
                    else:
                        pass

        if name_of_spaceaddict is not None:
            name = name_of_spaceaddict.lower()
            c.execute("SELECT * FROM spaceaddicts WHERE LOWER(name) = ?", (name,))
            result = c.fetchone()

            # If an exact result is found in spaceaddicts table, send it to the user
            if result:
                # Get the image from the local file system
                image_path = result[3]
                with open(image_path, 'rb') as f:
                    image_file = discord.File(f)

                # Create the embed
                embed = discord.Embed(
                    title=result[0],
                    description=result[2],
                    color=discord.Color.teal()
                )
                with Image.open(image_path) as img:
                    img = img.convert('RGB')  # convert the image mode to RGB
                    img.thumbnail((300, 300))
                    with io.BytesIO() as output:
                        img.save(output, format="JPEG")
                        image_data = output.getvalue()
                embed.set_image(url="attachment://thumbnail.png")
                embed.set_thumbnail(url="attachment://logoclear.png")
                embed.add_field(name="Title", value=result[1], inline=False)
                embed.set_footer(text=f"Learn more here: Spaceaddicts.io")

                # Send the message and the image files to the user
                await interaction.response.send_message(
                    embed=embed,
                    files=[
                        discord.File(io.BytesIO(image_data), filename='thumbnail.png'),
                        discord.File("logoclear.png", filename='logoclear.png')
                    ]
                )
            else:
                # Execute a SELECT statement using LIKE to search for similar items
                c.execute("SELECT *, 'spaceaddicts' as tablename FROM spaceaddicts WHERE LOWER(name) LIKE ? ", ('%'+name+'%',))
                results = c.fetchall()

                # If multiple results are found, suggest them to the user
                if results:
                    message_content = "Multiple items found..."
                    for r in results:
                        message_content += f"\n- {r[0]} ({r[4]})"
                    message_content += "\nPlease refine your search."
                    await interaction.response.send_message(message_content)
                else:
                    
                    pass
async def setup(bot):
    await bot.add_cog(searchrecords(bot))
