import discord
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected')

client.run(TOKEN)