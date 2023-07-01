import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)


class links(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.tree.command(name="links", description ="Show all official Space Addicts Links",)
    async def links(self, interaction: discord.Interaction):
        embed = discord.Embed(title=":pizza: :pizza: Space Addicts Links :pizza: :pizza:", color=0x00ff00)
        embed.set_thumbnail(url="attachment://logoclear.png")
        embed.add_field(name="COMIC BOOK PASS", value="https://app.manifold.xyz/c/GoldenArc", inline=False)
        embed.add_field(name="Official Twitter", value="https://twitter.com/SpaceAddictsNFT", inline=False)
        embed.add_field(name="Asteroid Belt Radio", value="https://twitter.com/Asteroid_Radio", inline=False)
        embed.add_field(name="Asteroid Belt Radio Youtube", value="https://youtube.com/@AsteroidBeltRadio", inline=False)
        embed.add_field(name="Website", value="https://www.spaceaddicts.io/", inline=False)
        embed.add_field(name="OpenSea", value="https://opensea.io/collection/space-addicts", inline=False)
        embed.add_field(name="Ron’s Tacklebox", value="https://opensea.io/collection/ronstacklebox", inline=False)
        embed.add_field(name="Ron’s Tacklebox V2 (PFP’s)", value="https://opensea.io/collection/ron-s-tacklebox-v2", inline=False)
        embed.add_field(name="High Quality Addicts", value="https://ipfs.io/ipfs/QmY3ygkfH16vSxsSRBxMtsVnBagraiCUfddzGU5yb7bdsL/4192.png (simply replace the token ID)", inline=False)
        await interaction.response.send_message(embed=embed, files=[discord.File("logoclear.png", filename='logoclear.png')])


async def setup(bot):
    await bot.add_cog(links(bot))
