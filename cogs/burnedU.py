import discord
from discord.ext import commands, tasks
import requests
import sqlite3

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)


class burned(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fetch_data_loop.start()  # Start the background task when the cog is initialized

    def cog_unload(self):
        self.fetch_data_loop.cancel()  # Cancel the background task when the cog is unloaded

    @bot.tree.command(
        name="burned",
        description="Manually trigger the update of NFT data in the database.",
    )
    async def burned(self, interaction: discord.Interaction):
        """
        Manually trigger the update of NFT data in the database.
        """
        await self.fetch_data()  # Call the fetch_data function to manually update the data
        await interaction.response.send_message("NFT data update completed.")

    @bot.tree.command(
        name="showalldead", description="Show all entries in the 'burned' database."
    )
    async def show_all_dead(self, ctx):
        """
        Show all entries in the 'burned' database.
        """
        try:
            connection = sqlite3.connect("viperdevmac.db")
            cursor = connection.cursor()

            cursor.execute("SELECT token_id, image_url, address FROM burned")
            entries = cursor.fetchall()

            channel = ctx.channel
            if channel:
                for entry in entries:
                    token_id, image_url, address = entry
                    embed = discord.Embed(
                        title=f"Transfer to {address}",
                        description=f"Token ID: {token_id}",
                        color=discord.Color.teal(),
                    )
                    embed.set_image(url=image_url)
                    await channel.send(embed=embed)

            connection.close()

        except Exception as e:
            print(f"An error occurred: {e}")
            await ctx.send(f"An error occurred: {e}")

    @tasks.loop(minutes=30)  # Fetch data every 30 minutes
    async def fetch_data_loop(self):
        await self.fetch_data()

    async def fetch_data(self):
        try:
            # Replace 'YOUR_OPENSEA_API_KEY' with your actual API key
            api_key = ""
            contract_address = "0x6184fAcb1850C8F7160Cc2F7BE8d2bC5192D3B70"
            url = f"https://api.opensea.io/api/v1/events?asset_contract_address={contract_address}&event_type=transfer&limit=100"
            headers = {"Accept": "application/json", "X-API-KEY": api_key}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                # Connect to the database and insert the new transfers
                connection = sqlite3.connect("viperdevmac.db")
                cursor = connection.cursor()

                for transfer in data["asset_events"]:
                    token_id = transfer["asset"]["token_id"]
                    image_url = transfer["asset"]["image_url"]
                    address = transfer["to_account"]["address"]

                    if address == "0x000000000000000000000000000000000000dead":
                        # Check if the record already exists in the database
                        cursor.execute(
                            """
                            CREATE TABLE IF NOT EXISTS burned
                            (token_id TEXT, image_url TEXT, address TEXT, sent TEXT)
                        """
                        )
                        cursor.execute(
                            "SELECT COUNT(*) FROM burned WHERE token_id = ?",
                            (token_id,),
                        )
                        count = cursor.fetchone()[0]

                        if count == 0:
                            print(
                                f"Token ID: {token_id}, Image URL: {image_url}, Address: {address}"
                            )

                            cursor.execute(
                                """
                                INSERT INTO burned (token_id, image_url, address)
                                VALUES (?, ?, ?)
                            """,
                                (token_id, image_url, address),
                            )

                            connection.commit()

                # Send new entries to the specified channel
                await self.send_new_entries()

        except Exception as e:
            print(f"An error occurred: {e}")

    async def send_new_entries(self):
        try:
            connection = sqlite3.connect("viperdevmac.db")
            cursor = connection.cursor()
            cursor.execute(
                "SELECT token_id, image_url, address FROM burned WHERE sent IS NULL"
            )
            entries = cursor.fetchall()

            channel_id = 1087039875410301009  # Replace with the actual channel ID
            channel = self.bot.get_channel(channel_id)
            if channel:
                for entry in entries:
                    token_id, image_url, address = entry
                    embed = discord.Embed(
                        title=f"Transfer to {address}",
                        description=f"Token ID: {token_id}",
                        color=discord.Color.teal(),
                    )
                    if image_url:
                        embed.set_image(url=image_url)
                    await channel.send(embed=embed)

                    # Mark sent entries as sent to avoid resending in the future
                cursor.execute("UPDATE burned SET sent = 1 WHERE sent IS NULL")
                connection.commit()
                if cursor.rowcount > 0:
                    print("Update successful.")
                else:
                    print("No rows updated.")

            connection.close()

        except Exception as e:
            print(f"An error occurred: {e}")

    @fetch_data_loop.before_loop
    async def before_fetch_data_loop(self):
        # Wait for the bot to be ready before starting the loop
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(burned(bot))
