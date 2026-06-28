from dotenv import load_dotenv
import os

load_dotenv()

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await message.channel.send("Hello!")


client.run(token=os.getenv("DISCORD_API_KEY"))