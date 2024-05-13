import discord
import os
from dotenv import load_dotenv
from discord.ext import commands, tasks
import random
import aiocron
import asyncio

import chessdotcom
from datetime import datetime


load_dotenv()

'''initialization'''
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
bot = commands.Bot(command_prefix='!', intents=intents)

chessdotcom.Client.request_config["headers"]["User-Agent"] = (
   "RPIChessBot"
   "Contact me at philippark271@gmail.com"
)


text_channel_list = []

mittens_quotes = [
    "meow",
    "Meow! I like chess, hehehe.",
    "I exist at this chess board through all times and realities. Hehehe. Meow." ,
    "*ominously* All chess players eventually crumble under my mighty paws…I mean, meow! Hehehe.",
    "I am a tiger and you are in the jungle I call eternity. Hehehe.",
    "*Knocks queen onto the floor* Your queen is gone. Hehehehe.",
    "Meow. That looks like a check. Hehehehe.",
    "It looks like I won, hehehe."
]

puzzle_post_time = "07:00:00"

@tasks.loop(minutes=1)
async def send_message():
    for guild in bot.guilds:
        if (guild.name != GUILD): 
            continue
        for channel in guild.text_channels:
            text_channel_list.append(channel.id)

    channel_id = random.choice(text_channel_list)
    channel = bot.get_channel(channel_id)
    dialogue = random.choice(mittens_quotes)
    await channel.send(dialogue)


@tasks.loop(seconds=1)
async def post_puzzle():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    if (current_time != puzzle_post_time):
        return
    
    response = chessdotcom.client.get_random_daily_puzzle().json['puzzle']
    print(response)

    title = response['title']
    image = response['image']
    url = response['url']
    fen = response['fen'].split()

    turn = "white to move" if (fen[1] == 'w') else "black to move"

    result_start = response['pgn'].index('1.')
    result = response['pgn'][result_start:-2]

    channel_id = 1238938678869622935
    channel = bot.get_channel(channel_id)

    await channel.send(f'{title}\nTurn: {turn}\n{image}\nSolution: ||{result}||')
    

'''events'''
@bot.event
async def on_ready():
    print(f'{bot.user} has connected')
    await post_puzzle()
    #send_message.start()
    post_puzzle.start()

    
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
            f.write(f'Unhandled message: : {args[0]}\n')
        else:
            raise
        
        

'''commands'''

'''
@bot.command(name = "quote", help="Responds with a random quote")
async def gotham_quote(ctx):
    quotes = ["What’s worth more than a Queen? You are",
          "Rook B1! Rook B1! Make a move! that makes no sense! That move literally is crazy! Why on earth would you play that!\nAt least castle your king! What the heck is this move? What are you trying to accomplish? I have no idea!",
          "You cannot stop an avalanche with a horse", "Have you ever been kicked in the face by a donkey?", "WHAT THE HELL IS D5???", "ble ble ble ble? ble ble ble blebleble?", "THE ROOOOOOK"]
    
    await ctx.send(random.choice(quotes))
'''

#echo a user response
@bot.command(help = "Echoes user input")
async def echo(ctx, arg):
    await ctx.send(arg)


#get stats on a profile
@bot.command(help = "Gives profile stats on a Chess.com username")
async def profile(ctx, given_username=commands.parameter(default="", description="Chess.com username")):
    response = {}

    try:
        response = chessdotcom.get_player_profile(given_username).json['player']
    except:
        await ctx.send("Chess.com username not found/missing. Usage: !profile username")
        return

    player_name = response['name'] if ('name' in response) else "None"
    username = response['username'] if ('username' in response) else "None"
    status = response['status'] if ('status' in response) else "None"
    is_streamer = response['is_streamer'] if ('is_streamer' in response) else "None"
    verified = response['verified'] if ('verified' in response) else "None"
    league = response['league'] if ('league' in response) else "None"

    stats = chessdotcom.client.get_player_stats(given_username).json['stats']

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
    
#get current daily puzzle
@bot.command(help='Gives the current daily puzzle')
async def daily_puzzle(ctx):
    response = chessdotcom.client.get_current_daily_puzzle().json['puzzle']
    title = response['title']
    image = response['image']
    url = response['url']
    fen = response['fen'].split()

    turn = "white to move" if (fen[1] == 'w') else "black to move"

    result_start = response['pgn'].index('\n1.')
    result = response['pgn'][result_start+1:]

    await ctx.send(f'{title}\nTurn: {turn}\n{image}\nSolution: ||{result}||')

#get random daily puzzle
@bot.command(help='Gives a random daily puzzle')
async def puzzle(ctx):
    response = chessdotcom.client.get_random_daily_puzzle().json['puzzle']
    title = response['title']
    image = response['image']
    url = response['url']
    fen = response['fen'].split()

    turn = "white to move" if (fen[1] == 'w') else "black to move"

    result_start = response['pgn'].index('\n1.')
    result = response['pgn'][result_start+1:-2]

    await ctx.send(f'{title}\nTurn: {turn}\n{image}\nSolution: ||{result}||')


#randomly choose a club member
@bot.command(help="Randomly chooses a club member with no membership")
async def lottery(ctx):
    members = chessdotcom.client.get_club_members('rensselaer-chess-club', 0).json['members']

    no_memberships = []

    for member in members['all_time']:
        try:
            username = member['username']
            profile = chessdotcom.get_player_profile(username).json['player']

            if ('status' in profile):
                if (profile['status'] == 'basic'):
                    no_memberships.append(username)
        except:
            pass
    
    await ctx.send(random.choice(no_memberships))


categories = ["daily", "daily960","live_rapid","live_blitz","live_bullet","live_bughouse","live_blitz960","live_threecheck","live_crazyhouse","live_kingofthehill","tactics","rush","battle"]
#get top 5 on leaderboard for given category
@bot.command(help="Gives global top 5 on Chess.com for a category")
async def leaderboard(ctx, category=commands.parameter(default="", description=" ".join(categories))):

    leaderboard = chessdotcom.client.get_leaderboards().json['leaderboards']

    top_5 = f'Top 5 for {category}:\n'

    if category in leaderboard:
        catergory_leaderboard = leaderboard[category][:5]

        i = 1
        for player in catergory_leaderboard:
            top_5 += (f'{i}. ' + player['username'] + '\n')
            i+=1

        await ctx.send(top_5)
        
    
    else:
        await ctx.send('Invalid/missing category. Categories: ' + leaderboard.keys())

#get top 5 on club leaderboard for given category
@bot.command(help="IN DEVELOPMENT")
async def club_leaderboard(ctx, category=commands.parameter(default="", description=" ".join(categories))):
    '''
    leaderboard = chessdotcom.client.get_leaderboards().json['leaderboards']

    top_5 = f'Top 5 for {category}:\n'

    if category in leaderboard:
        catergory_leaderboard = leaderboard[category][:5]

        i = 1
        for player in catergory_leaderboard:
            top_5 += (f'{i}. ' + player['username'] + '\n')
            i+=1

        await ctx.send(top_5)
        
    
    else:
        await ctx.send('Invalid/missing category. Categories: ' + leaderboard.keys())
    '''

    members = chessdotcom.client.get_club_members('rensselaer-chess-club', 0).json['members']

    ratings = []

    for member in members['all_time']:
        username = member['username']
        stats = chessdotcom.client.get_player_stats(username).json['stats']
        blitz_rating = stats['chess_blitz']['last']['rating'] if ('chess_blitz' in stats) else 'None'

        if (blitz_rating == 'None'):
            continue

        ratings.append((int(blitz_rating), username))
    
    ratings.sort(reverse=True)

    top_5 = f'Top 5 for {category}:\n'
    
    for player in ratings:
            top_5 += (f'{player[1]}. ' + str(player[0]) + '\n')

    await ctx.send(top_5)

    print(ratings)

    


log = dict()

@bot.command()
async def log_member_stats(ctx, help="In Development"):
    members = chessdotcom.client.get_club_members('rensselaer-chess-club', 0).json['members']

    for member in members['all_time']:
        username = member['username']
        stats = chessdotcom.client.get_player_stats(username).json['stats']
        blitz_rating = stats['chess_blitz']['last']['rating'] if ('chess_blitz' in stats) else 'None'

        if (blitz_rating == 'None'):
            continue

        log[username] = int(blitz_rating)
    
    await ctx.send(log)
    print(log)

diff = dict()
@bot.command()
async def get_member_stats(ctx, help="In Development"):
    members = chessdotcom.client.get_club_members('rensselaer-chess-club', 0).json['members']

    for member in members['all_time']:
        username = member['username']
        stats = chessdotcom.client.get_player_stats(username).json['stats']
        blitz_rating = stats['chess_blitz']['last']['rating'] if ('chess_blitz' in stats) else 'None'

        if (blitz_rating == 'None'):
            continue
        if (username not in log):
            continue

        diff[username] = log[username] - int(blitz_rating)
    
    await ctx.send(diff)
    print(diff)



if __name__ == "__main__":
    bot.run(TOKEN)
