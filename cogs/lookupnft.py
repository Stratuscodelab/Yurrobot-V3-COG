import discord
import io
from discord.ext import commands
from PIL import Image
import json
from discord import app_commands
import asyncio
from discord.embeds import Embed

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)



class lookupnft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @bot.tree.command(name="lookupnft", description="Lookup any SpaceAddict NFT by number")
    async def lookupnft(self, interaction: discord.Interaction, lookup_this_number: int = None):
        if lookup_this_number is not None:
            if isinstance(lookup_this_number, int):
                if lookup_this_number in range(1, 5556):
                    with open("sametar.json", "r") as f:
                        data = json.load(f)

                    nfts = data
                    nft_data = None
                    for nft in nfts:
                        if nft["edition"] == lookup_this_number:
                            nft_data = nft
                            break

                    if nft_data:
                        embed = Embed(title=f"Attributes for Edition {lookup_this_number}", description="", color=0x00ff00)
                        embed.set_thumbnail(url="attachment://logoclear.png")
                        for attribute in nft_data["attributes"]:
                            embed.add_field(name=attribute['trait_type'], value=attribute['value'], inline=False)
                        embed.set_image(url=nft_data['image'])
                        await interaction.response.send_message(embed=embed, 
                                            files=[discord.File("logoclear.png", filename='logoclear.png')])
                    else:
                        await interaction.response.send_message(f"No NFT found for edition {lookup_this_number}.")
                else:
                    await interaction.response.send_message("Invalid input. Please enter a number between 1 and 5555.")
            else:
                await interaction.response.send_message("Invalid input. Please enter a number.")
        else:
            await interaction.response.send_message("Please provide a number to lookup the NFT.")

            
            
            
async def setup(bot):
    await bot.add_cog(lookupnft(bot))