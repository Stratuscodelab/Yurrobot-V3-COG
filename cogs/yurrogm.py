import discord
from discord.ext import commands
from PIL import Image
import os
import datetime
import asyncio

intents = discord.Intents.all()
intents.messages = True

# Menu system for the meme maker
# Define the directory for the overlay images
overlay_directory = "overlay_images"

overlay_options = {
    "1": {"image": "Coffee-GM.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "2": {"image": "Cipher-Badge.png", "allowed_roles": [1031246673281830943, 962415058284056626]},
    "3": {"image": "King-Pizza-Badge", "allowed_roles": [1031246847509012573, 962415058284056626]},
    "4": {"image": "Sokan-Badge.png", "allowed_roles": [1031246479182004264, 962415058284056626]},
    "5": {"image": "BadBones-Badge.png", "allowed_roles": [990459796106928128, 962415058284056626]},
    "6": {"image": "Uncle-Sals.png", "allowed_roles": [1031246244116430848, 962415058284056626]},
    "7": {"image": "Dual-lightening.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "8": {"image": "Broken-Visor.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "8": {"image": "GM-big.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "9": {"image": "GM-digital.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "10": {"image": "GM-digital.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "11": {"image": "GN-blue.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "12": {"image": "GN-digital.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "13": {"image": "Good-Job-Bro.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "14": {"image": "I_Love_nfts.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "15": {"image": "neon-pizza.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "16": {"image": "PIZZA-PARTY.png", "allowed_roles": [962419808308183100,962415058284056626]},
    "17": {"image": "Visor-Blue-Blazer.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "18": {"image": "Visor-Green-Drink.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "19": {"image": "Visor-Mello-Yellow.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "20": {"image": "Visor-Orange-Juice.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "21": {"image": "Witch-Hunter-Hat.png", "allowed_roles": [962419808308183100, 962415058284056626]},
    "22": {"image": "SpaceAddicts-Badge.png", "allowed_roles": [962419808308183100, 962415058284056626]},




}

# Update the overlay options with the full paths to the images this one for windows server.
# overlay_directory = rD:\\YurroBot\\SpaceAddicts-YurroBot-main\\v3\\overlay_images

overlay_directory = "D:\\YurroBot\\SpaceAddicts-YurroBot-main\\v3\\overlay_images"  # Update with the directory containing overlay images

for key, value in overlay_options.items():
    value["image"] = os.path.join(overlay_directory, value["image"])

bot = commands.Bot(command_prefix="/", intents=intents)

class yurrogm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.tree.command(name="yurrogm", description="The famous Yurrobot image modification service")
    async def yurrogm(self, interaction: discord.Interaction):
        def check(message):
            return message.author == interaction.user and message.channel == interaction.channel

        await interaction.response.send_message(content="Please upload your image.", ephemeral=True)

        try:
            message = await self.bot.wait_for("message", timeout=60.0, check=check)
            if len(message.attachments) == 0:
                return await interaction.followup.send(content="No image file uploaded.", ephemeral=True)

            attachment = message.attachments[0]
            allowed_formats = ['.png', '.jpg', '.jpeg']

            if not any(attachment.filename.lower().endswith(format) for format in allowed_formats):
                await interaction.followup.send(content='Please upload a PNG or JPEG image.', ephemeral=True)
                return

            # Download the uploaded image
            await attachment.save(attachment.filename)

            # Resize the image to 612x612 pixels
            resized_image = Image.open(attachment.filename)
            resized_image = resized_image.resize((612, 612), Image.LANCZOS)

            # Create an embed with the menu options
            embed = discord.Embed(
                title="Overlay Options",
                description="Please select an overlay option by typing a number (e.g., `1`, `2`, etc.):",
                color=discord.Color.teal()
            )
            for option, overlay_info in overlay_options.items():
                overlay_filename = os.path.basename(overlay_info["image"])
                embed.add_field(name=f"Option {option}", value=overlay_filename, inline=False)

            # Send the embed as a menu prompt (ephemeral)
            menu_message = await interaction.followup.send(embed=embed, ephemeral=True)

            def check_option(m):
                return m.author == interaction.user and m.channel == interaction.channel

            try:
                overlay_option = await self.bot.wait_for('message', check=check_option, timeout=60)
            except asyncio.TimeoutError:
                await interaction.followup.send(content="Timeout: No option selected.", ephemeral=True)
                return

            selected_option = overlay_option.content.strip()

            if selected_option not in overlay_options:
                await interaction.followup.send(content="Invalid overlay option selected.", ephemeral=True)
                return

            selected_overlay = overlay_options[selected_option]
            allowed_roles = selected_overlay["allowed_roles"]
            has_allowed_role = any(role.id in allowed_roles for role in interaction.user.roles)

            if not has_allowed_role:
                await interaction.followup.send(content="You don't have permission to use this overlay option.", ephemeral=True)
                return

            # Apply the selected overlay to the resized image
            overlay_image = Image.open(selected_overlay["image"])
            resized_image.paste(overlay_image, (0, 0), overlay_image)

            # Generate a unique filename for the modified image
            creator_name = interaction.user.name.replace(" ", "_")
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            result_filename = f'{creator_name}_{timestamp}.png'

            # Define the directory to save the file
            save_directory = "yurromeme"
            os.makedirs(save_directory, exist_ok=True)

            # Specify the full path to save the file
            save_path = os.path.join(save_directory, result_filename)

            # Save the modified image
            resized_image.save(save_path)

            # Clean up temporary files
            resized_image.close()
            overlay_image.close()
            os.remove(attachment.filename)

            # Delete the message containing the uploaded image and the menu selection
            await message.delete()
            await overlay_option.delete()

            # Upload the modified image back to Discord without the "Please upload your image" message (ephemeral)
            result_image = discord.File(save_path)
            await interaction.followup.send(
                content="Here is your modified image!",
                file=result_image,
                ephemeral=True
            )

        except asyncio.TimeoutError:
            await interaction.followup.send(content="Command timed out.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(yurrogm(bot))


