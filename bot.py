from dotenv import load_dotenv
import os

load_dotenv()

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


client.run(token=os.getenv("DISCORD_API_KEY"))