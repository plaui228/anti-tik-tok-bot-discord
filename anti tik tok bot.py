import discord
import re
import datetime

BOT_TOKEN = "YOUR DISCORD BOT TOKEN"  # Replace with your actual bot token

TARGET_CHANNEL_ID = "YOURE LINKS CHANNEL ID"

DELETE_CHANNEL_ID = "YOUR MAIN CHANNEL ID"

sent = None
file_name = "tiktok_urls.txt"  # Name of the file to store URLs

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
client = discord.Client(intents=intents)

# List of common TikTok subdomains and pattern for vm.tiktok.com links
tiktok_subdomains = [
    "https://www.tiktok.com",
    "@tiktok.com",
    "www.tiktok.com",
]
vm_tiktok_pattern = r"^https?://vm\.tiktok\.com/.*$"  # Regular expression for vm.tiktok.com links


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print("message detected")

    # Get current date and time
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")  # Format: YYYY-MM-DD HH:MM:SS

    # Check for full URLs using subdomain list
    for subdomain in tiktok_subdomains:
        if subdomain.lower() in message.content.lower():
            print("TikTok URL detected (full URL)")
            url = message.content  # Extract URL for writing to file and potentially sending

            # Write URL and timestamp to file
            with open(file_name, "a") as f:
                f.write(f"{formatted_datetime} - {url}\n")  # Append new URL with timestamp
            print(f"Wrote TikTok URL ({url}) with timestamp to {file_name}")

            if TARGET_CHANNEL_ID is not None:  # Check if target channel is configured
                target_channel = await client.fetch_channel(TARGET_CHANNEL_ID)
                if target_channel is not None:
                    await target_channel.send(url)
                    print(f"Message content sent to target channel: {url}")
                    if DELETE_CHANNEL_ID is not None:  # Check if delete channel is configured
                        delete_channel = await client.fetch_channel(DELETE_CHANNEL_ID)
                        if delete_channel is not None:
                            await message.delete()
                            print(f"Deleted message with TikTok URL: {url}")
                else:
                    print(f"Error: Channel with ID {TARGET_CHANNEL_ID} not found.")
            else:
                print("Target channel not configured for sending messages.")
            return  # Exit the loop after detecting a full URL

    # Check for vm.tiktok.com links using regular expression
    vm_tiktok_match = re.match(vm_tiktok_pattern, message.content)
    if vm_tiktok_match:
        print("TikTok URL detected (vm.tiktok.com)")
        url = message.content  # Extract URL for writing to file and potentially sending

        # Write URL and timestamp to file
        with open(file_name, "a") as f:
            f.write(f"{formatted_datetime} - {url}\n")  # Append new URL with timestamp
        print(f"Wrote TikTok URL ({url}) with timestamp to {file_name}")

        if TARGET_CHANNEL_ID is not None:  # Check if target channel is configured
            target_channel = await client.fetch_channel(TARGET_CHANNEL_ID)
            if target_channel is not None:
                await target_channel.send(url)
                print(f"Message content sent to target channel: {url}")
                if DELETE_CHANNEL_ID is not None:  # Check if delete channel is configured
                    delete_channel = await client.fetch_channel(DELETE_CHANNEL_ID)
                    if delete_channel is not None:
                        await message.delete()
                        print(f"Deleted message with TikTok URL: {url}")
                else:
                    print("Delete channel not configured for message deletion.")
            else:
                print(f"Error: Channel with ID {TARGET_CHANNEL_ID} not found.")
        else:
            print("Target channel not configured for sending messages.")
        return  # Exit the loop after detecting a vm.tiktok.com link

    print("No TikTok URL detected")  # Optional for logging


client.run(BOT_TOKEN)