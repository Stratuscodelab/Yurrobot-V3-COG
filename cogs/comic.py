import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)


class Comic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.tree.command(name="comic", description ="How to view the SpaceAddicts digital Comic",)
    async def links(self, interaction: discord.Interaction):
        embed = discord.Embed(title=":reg: Comic :reg:", description="How to view the comic", color=0xffcc00)
        embed.set_thumbnail(url="attachment://logoclear.png")
        embed.add_field(name="", value="You can now visit this link https://vault.spaceaddicts.io/ or click on the comic link at Spaceaddicts.io. Connect you wallet and if you own the NFT it will show you the unlockable content. ", inline=False)
        embed.add_field(name="", value="You will notice 4 files there. Only read the PDF's. The JPEG files are too small and the PDF gives you the ability to zoom in and read it. ", inline=False)
        embed.add_field(name="DO NOT SHARE ANY OF THE COMIC BOOK PAGES. FOR YOUR EYES ONLY. IT IS HOW WE ADD VALUE TO HOLDING NFT'S IN OUR COLLECTION. ", value="", inline=False)
        embed.add_field(name="", value="For those of you that are new we have our weekly twitter space tonight at 8pm EST. Please join in and feel free to pop up and chat. \n \n https://twitter.com/SpaceAddictsNFT/status/1637479539147194370?s=20 \n \n Thanks to all that have purchased the comic so far!", inline=False)
        embed.add_field(name="-Steve #stayhungry", value="", inline=False)
        await interaction.response.send_message(embed=embed, files=[discord.File("logoclear.png", filename='logoclear.png')])
        


async def setup(bot):
    await bot.add_cog(Comic(bot))
