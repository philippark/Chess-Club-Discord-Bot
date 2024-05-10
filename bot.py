import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random

load_dotenv()

#intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#initialization
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(intents=intents, command_prefix="!")

quotes = ["What’s worth more than a Queen? You are",
          "Rook B1! Rook B1! Make a move! that makes no sense! That move literally is crazy! Why on earth would you play that!\nAt least castle your king! What the heck is this move? What are you trying to accomplish? I have no idea!",
          "You cannot stop an avalanche with a horse", "Have you ever been kicked in the face by a donkey?", "WHAT THE HELL IS D5???", "ble ble ble ble? ble ble ble blebleble?", "THE ROOOOOOK"]

#events
@bot.event
async def on_ready():
    print(f'{bot.user} has connected')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "/gotham_quote":
        await message.channel.send(random.choice(quotes))

    elif message.content == "raise-exception":
        raise discord.DiscordException

@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Ladies and Gentlemen, {member.mention} has arrived to {guild.name}!'
        await guild.system_channel.send(to_send)

@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

bot.run(TOKEN)