import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Custom Library's
import challonge_tournament
from time_conversion import get_checkin_time

# Get Information for .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_Key = os.getenv('API_V1')
USERNAME = os.getenv('CHALLONGE_USERNAME')
current_tournament = os.getenv('TOURNAMENT')

# Set Challonge Credentials
challonge_tournament.set_creds(USERNAME, API_Key)
# Get Current Tournament
tournament = challonge_tournament.get_tournament(current_tournament)
# Name of the Tournament
tournament_name = challonge_tournament.tournament_name(tournament)
# Start Time of Tournament
tournament_time = challonge_tournament.tournament_start_time(tournament)
# Get Current Round

# Define the bot and its command prefix
intents = discord.Intents.default()
intents.message_content = True  # To allow the bot to read message content

bot = commands.Bot(command_prefix="_", intents=intents)


# Event for when the bot has connected to Discord
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Command that the bot will respond to with "Pong!"
@bot.command(name="fighters")
async def fighters(ctx):
    # Get Participants
    players = challonge_tournament.get_participants(tournament)
    for player in players:
        await ctx.send(player)

@bot.command(name="begin")
async def begin(ctx):
    await ctx.send("Tournament: " + tournament_name)
    await ctx.send("Start Date and Time: " + tournament_time)
    minutes = tournament['check_in_duration']
    if minutes:
        checkin_time = get_checkin_time(tournament_time, minutes)
        await ctx.send("Checkin Date and Time: " + checkin_time)


@bot.command(name="matches")
async def get_matches(ctx):
    # Get matches
    matches = challonge_tournament.get_matches(tournament, current_tournament)
    round = 1
    if matches:
        for players in matches:
            await ctx.send("Match: " + str(round))
            await ctx.send(players[0] + " VS " + players[1])
            if len(players) == 3:
                await ctx.send("Winner: " + players[2])
            if len(matches) >= round:
                round = len(matches)
            else:
                round += 1
    else:
        await ctx.send("Tournament Has Not Started!!")
        await ctx.send("Start Date and Time: " + tournament_time)

@bot.command(name="register")
async def register(ctx):
    if tournament['state'] == 'pending':
        register_url = challonge_tournament.register_url(tournament)
        await ctx.send("Register @ " + register_url)
    else:
        await ctx.send("Tournament Has Started!!")

# Run the bot
bot.run(TOKEN)