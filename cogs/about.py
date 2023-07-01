import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)


class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.tree.command(name="about", description ="Show all information about SpaceAddicts",)
    async def links(self, interaction: discord.Interaction):
        embed = discord.Embed(title="The World: 🪐", description="The Year: Who cares.... IT'S OUTER SPACE. It's... kinda hard to live.", color=0xffcc00)
        embed.set_thumbnail(url="attachment://logoclear.png")
        embed.add_field(name="The (Space Addicts) :reg: Fight to Survive", value="With sparse resources and an empty stomach, the (Space Addicts) fight to survive. There are no planets left in the solar system. The only safe place is on your battleships, and maybe an asteroid city (if you're lucky).\n\nLet's not forget your empty stomach. PIZZA:ShrimpDelight: is the only thing that keeps us alive! It's really the only blueprint we could find... Then we all decided that Pizza Rocks! Why make anything else...", inline=False)
        embed.add_field(name="5 Pizza Factions Fight for Supremacy", value="5 PIZZA FACTIONS:badbones: :cipher: :kingpizza: :sals: :sokan: fight for pizza supremacy while the rest of the Galaxy lives and works. If you can find a steady job, keep it. If you can find a good crew, bare arms with them. Constant battles rage on in and out of every day and night cycle. It's pretty normal at this point.", inline=False)
        embed.add_field(name="The Only Problem: Low Fuel Cells!", value="Fuel Cells power everything. You have to fight to get your hands on one. If you can produce them, well you're asking for a bruis'n! The whole galaxy is hungry for Pizza, Fuel Cells, and all out War...no big deal right?", inline=False)
        embed.add_field(name="Choose Your Character Wisely", value="Be careful out there. Choose your Character wisely. Pack the right heat. Grab the best slice.:Onionsupreme: :ShrimpDelight: :TropicalThunder: `:pizza~1:` Join the fight and fight to survive.:sword:", inline=False)
        await interaction.response.send_message(embed=embed, files=[discord.File("logoclear.png", filename='logoclear.png')])
        


async def setup(bot):
    await bot.add_cog(About(bot))
