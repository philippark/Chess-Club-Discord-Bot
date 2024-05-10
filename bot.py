import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random

from chessdotcom import get_player_profile, Client
import chessdotcom


load_dotenv()

#intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

#initialization
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='!', intents=intents)

Client.request_config["headers"]["User-Agent"] = (
   "My Python Application. "
   "Contact me at email@example.com"
)

#events
@bot.event
async def on_ready():
    print(f'{bot.user} has connected')
    
@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Ladies and Gentlemen, {member.mention} has arrived to {guild.name}!'
        await guild.system_channel.send(to_send)

#commands
@bot.command(name = "quote", help="Responds with a random quote")
async def gotham_quote(ctx):
    quotes = ["What’s worth more than a Queen? You are",
          "Rook B1! Rook B1! Make a move! that makes no sense! That move literally is crazy! Why on earth would you play that!\nAt least castle your king! What the heck is this move? What are you trying to accomplish? I have no idea!",
          "You cannot stop an avalanche with a horse", "Have you ever been kicked in the face by a donkey?", "WHAT THE HELL IS D5???", "ble ble ble ble? ble ble ble blebleble?", "THE ROOOOOOK"]
    
    await ctx.send(random.choice(quotes))

@bot.command()
async def echo(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def profile(ctx, arg):
    try:
        response = get_player_profile(arg)
        player_name = response.player.name

        await ctx.send(f'Name: {response.player.name}\nUsername: {response.player.username}\nCountry: {response.player.country}\nLast Online: {response.player.last_online}')
    except:
        await ctx.send("Chess.com username not found")

@bot.command()
async def daily_puzzle(ctx, arg):
    puzzle = chessdotcom.client.get_current_daily_puzzle
    await ctx.send(puzzle)

bot.run(TOKEN)