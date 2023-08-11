import discord
import io
from discord.ext import commands
from PIL import Image
import json
from discord import app_commands
import asyncio
from discord.embeds import Embed
import psutil
import datetime
import os
import sqlite3

intents = discord.Intents.all()
intents.messages = True
start_time = datetime.datetime.utcnow()

conn = sqlite3.connect('viperdevmac.db')
c = conn.cursor()

bot = commands.Bot(command_prefix="/", intents=intents)

def get_directory_size(directory):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

# Function to convert bytes to megabytes
def convert_bytes_to_megabytes(bytes):
    megabytes = bytes / (1024 * 1024)
    return megabytes



class yurrostats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        

    @bot.tree.command(name="yurrostats", description="Displays YurroBot server stats")
    async def yurrostats(self, interaction: discord.Interaction):
        # CPU and memory usage
        cpu_usage = psutil.cpu_percent()
        mem_usage = psutil.virtual_memory().percent

        # Database records
        c.execute("SELECT COUNT(*) FROM spaceaddicts")
        num_records = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM ront")
        num_records2 = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM shop")
        num_records3 = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM MemoryProtocol")
        num_records4 = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM burned")
        num_records5 = c.fetchone()[0]

        # Server information
        total_users = len(set(interaction.guild.members))
        total_channels = len(interaction.guild.channels)

        # Uptime
        uptime = datetime.datetime.utcnow() - start_time
        uptime_str = str(uptime).split(".")[0]

        # Network speed
        net_io_counters = psutil.net_io_counters()
        bytes_sent = net_io_counters.bytes_sent
        bytes_recv = net_io_counters.bytes_recv

        # Wait for 1 second to get a more accurate measurement
        await asyncio.sleep(1)

        net_io_counters = psutil.net_io_counters()
        bytes_sent_diff = net_io_counters.bytes_sent - bytes_sent
        bytes_recv_diff = net_io_counters.bytes_recv - bytes_recv
        net_speed = f"Download Speed: {bytes_recv_diff / 1024:.2f} KB/s, Upload Speed: {bytes_sent_diff / 1024:.2f} KB/s"

        # Directory sizes
        yurromeme_size_bytes = get_directory_size("yurromeme")
        dmlog_size_bytes = get_directory_size("DMlog")

        # Convert bytes to megabytes
        yurromeme_size_mb = convert_bytes_to_megabytes(yurromeme_size_bytes)
        dmlog_size_mb = convert_bytes_to_megabytes(dmlog_size_bytes)

        # Version number
        version_num = "3.2 - Cog - 2023- MemoryProtocol Initiated"

        # Build server stats and bot stats strings
        server_stats = (
            f"CPU usage: {cpu_usage}%\n"
            f"Memory usage: {mem_usage}%\n"
            f"Number of SA Database Records: {num_records}\n"
            f"Number of Ron Tacklebox Database Records: {num_records2}\n"
            f"Number of Shop Database Records: {num_records3}\n"
            f"Number of Memory Protocol Characters: {num_records4}\n"
            f"Number of Burned Space Addicts: {num_records5}\n"
            f"Yurromeme Directory Size: {yurromeme_size_mb:.2f} MB\n"
            f"DMlog Directory Size: {dmlog_size_mb:.2f} MB"
        )

        bot_stats = (
            f"Total users: {total_users}\n"
            f"Total channels: {total_channels}\n"
            f"Bot Uptime: {uptime_str}\n"
            f"{net_speed}\n"
            f"Yurrobot Version: {version_num}"
        )

        # Create embed
        embed = discord.Embed(title="Server and Bot Stats", color=0x00ff00)
        embed.set_thumbnail(url="attachment://logoclear.png")
        embed.add_field(name="Server Stats", value=server_stats, inline=False)
        embed.add_field(name="Bot Stats", value=bot_stats, inline=False)

        await interaction.response.send_message(embed=embed, files=[discord.File("logoclear.png", filename='logoclear.png')])

        
        
async def setup(bot):
    await bot.add_cog(yurrostats(bot))
