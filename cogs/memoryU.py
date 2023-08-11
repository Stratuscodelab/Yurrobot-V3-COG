import discord
from discord.ext import commands, tasks
import requests
import sqlite3

intents = discord.Intents.all()
intents.messages = True

bot = commands.Bot(command_prefix="/", intents=intents)


class UpdateRecords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.tree.command(
        name="updaterecords",
        description="Updates any missing values in the MemoryProtocol database",
    )
    async def updaterecords(self, interaction: discord.Interaction):
        """
        Manually trigger the update of NFT data in the database.
        Usage: /update_nft_data
        """
        await self.fetch_data()  # Call the fetch_data function to manually update the data
        await interaction.response.send_message("NFT data update completed.")

    @tasks.loop(
        minutes=30
    )  # Fetch data every 30 minutes, you can adjust the interval as needed
    async def fetch_data(self):
        try:
            # Replace 'YOUR_OPENSEA_API_KEY' with your actual API key
            api_key = ""
            token_id = "space-addicts-memory-protocol"
            url = f"https://api.opensea.io/v2/collection/{token_id}/nfts"
            headers = {"Accept": "application/json", "X-API-KEY": api_key}

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                # Assuming the response contains a list of NFTs, you can loop through them
                new_nfts = []  # List to store new NFTs that are not yet in the database
                for nft in data["nfts"]:
                    # Extract relevant data from each NFT
                    name = nft["name"]
                    description = nft["description"]
                    image = nft["image_url"]

                    # Check if the image URL exists, if not, set it to None (NULL)
                    if not image.startswith("http"):
                        image = None

                    # Connect to the SQLite database
                    connection = sqlite3.connect("viperdevmac.db")
                    cursor = connection.cursor()

                    # Check if the entry already exists in the 'MemoryProtocol' table
                    cursor.execute(
                        """
                        SELECT name FROM MemoryProtocol WHERE name = ? AND description = ?
                    """,
                        (name, description),
                    )
                    existing_entry = cursor.fetchone()

                    if existing_entry is None:
                        # Add the NFT data to the list of new NFTs
                        new_nfts.append((name, description, image))

                    connection.close()

                # Connect to the database again to insert the new NFTs
                connection = sqlite3.connect("viperdevmac.db")
                cursor = connection.cursor()

                # Create the 'MemoryProtocol' table if it doesn't exist
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS MemoryProtocol
                    (name TEXT, description TEXT, image TEXT)
                """
                )

                # Insert the new NFTs into the 'MemoryProtocol' table
                cursor.executemany(
                    """
                    INSERT INTO MemoryProtocol (name, description, image)
                    VALUES (?, ?, ?)
                """,
                    new_nfts,
                )

                connection.commit()
                connection.close()

                # Return the new NFTs to be used for updating NULL image URLs
                return new_nfts

        except Exception as e:
            print(f"An error occurred: {e}")

    @fetch_data.before_loop
    async def update_image_urls(self, new_nfts):
        """
        Update the image URLs for NULL records in the 'MemoryProtocol' table.
        """
        try:
            connection = sqlite3.connect("viperdevmac.db")
            cursor = connection.cursor()

            for name, description, image in new_nfts:
                if image is None:
                    api_key = ""
                    token_id = "space-addicts-memory-protocol"
                    url = f"https://api.opensea.io/v2/collection/{token_id}/nfts/{name}"
                    headers = {"Accept": "application/json", "X-API-KEY": api_key}

                    response = requests.get(url, headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        image_url = data["image_url"]
                        print(f"Updating image URL for: {name}, {description}")
                        print(f"Old image URL: {image}")
                        print(f"New image URL: {image_url}")
                        # Update the NULL record in the 'MemoryProtocol' table with the image URL
                        cursor.execute(
                            """
                            UPDATE MemoryProtocol SET image = ? WHERE name = ? AND description = ? AND image IS NULL
                        """,
                            (image_url, name, description),
                        )

            # Commit the changes after updating all records with NULL images
            connection.commit()
            connection.close()

        except Exception as e:
            print(f"An error occurred while updating image URLs: {e}")


async def setup(bot):
    await bot.add_cog(UpdateRecords(bot))
