import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import random

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

chessdotcom.Client.request_config["headers"]["User-Agent"] = (
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
    response = {}

    try:
        response = chessdotcom.get_player_profile(arg).json['player']
    except:
        await ctx.send("Chess.com username not found")

    player_name = response['name'] if ('name' in response) else "None"
    username = response['username'] if ('username' in response) else "None"
    status = response['status'] if ('status' in response) else "None"
    is_streamer = response['is_streamer'] if ('is_streamer' in response) else "None"
    verified = response['verified'] if ('verified' in response) else "None"
    league = response['league'] if ('league' in response) else "None"

    

    stats = chessdotcom.client.get_player_stats(username).json['stats']

    rapid = stats['chess_rapid']['last']['rating'] if ('chess_rapid' in stats) else 'None'
    blitz = stats['chess_blitz']['last']['rating'] if ('chess_blitz' in stats) else 'None'

    await ctx.send(f'Name: {player_name}\n'+
                       f'Username: {username}\n'+
                       f'Status: {status}\n'+
                       f'is_streamer: {is_streamer}\n'+
                       f'verified: {verified}\n'+
                       f'league: {league}\n'+
                       f'rapid: {rapid}\n'+
                       f'blitz: {blitz}'
                       )
    
@bot.command()
async def daily_puzzle(ctx):
    response = chessdotcom.client.get_current_daily_puzzle()
    title = response.puzzle.title
    image = response.puzzle.image
    url = response.puzzle.url

    await ctx.send(f'{title} {image}')

bot.run(TOKEN)