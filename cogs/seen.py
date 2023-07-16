import discord
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)

class Seen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_seen = {}

    @bot.tree.command()
    async def seen(self, interaction: discord.Interaction, user: discord.Member):
        if user.id in self.last_seen:
            last_seen = self.last_seen[user.id]
            last_seen_str = last_seen["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            last_message = last_seen["message"]
            last_channel = self.bot.get_channel(last_seen["channel"])

            embed = discord.Embed(title="Last Seen", color=discord.Color.blue())
            embed.set_author(name=user.name, icon_url=user.avatar.url)
            embed.add_field(name="Last seen on", value=last_seen_str)
            embed.add_field(name="Last known message", value=last_message)
            embed.add_field(name="Last seen in", value=last_channel.mention)

            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(f"{user.name} has not been seen recently")

    @commands.Cog.listener()
    async def on_message(self, message):
        user_id = message.author.id
        self.last_seen[user_id] = {
            "timestamp": datetime.now(),
            "message": message.content,
            "channel": message.channel.id
        }

async def setup(bot):
    await bot.add_cog(Seen(bot))

