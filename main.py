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
bot_test_id = int(os.getenv('BOT_TEST')) # Test Channel
main_id = int(os.getenv('MAIN')) # Maniacs Tournament
bracket_id = int(os.getenv('BRACKET')) # Tournament Bracket
char_select_id = int(os.getenv('CHARACTER_SELECT')) # Character Select

# Set Challonge Credentials
challonge_tournament.set_creds(USERNAME, API_Key)
# Get Current Tournament
tournament = challonge_tournament.get_tournament(current_tournament)
# Name of the Tournament
tournament_name = challonge_tournament.tournament_name(tournament)
# Start Time of Tournament
tournament_time = challonge_tournament.tournament_start_time(tournament)


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
    # Check if the call is in the Character Select Channel
    if ctx.channel.id in [char_select_id, bot_test_id]:
        players = challonge_tournament.get_participants(tournament)
        for player in players:
            await ctx.send(player[0] + " as " + player[1])


# Command that the bot will respond to with "Pong!"
@bot.command(name="players")
async def players(ctx):
    # Get Participants
    # Check if the call is in the Maniacs Tournament and Tournament Bracket Channels
    if ctx.channel.id in [main_id, bracket_id, bot_test_id]:
        players = challonge_tournament.get_participants(tournament)
        for player in players:
            await ctx.send(player[0])


@bot.command(name="begin")
async def begin(ctx):
    # Check if the call is in the Maniacs Tournament Channel
    if ctx.channel.id in [main_id, bot_test_id]:
        await ctx.send("Tournament: " + tournament_name)
        await ctx.send("Start Date and Time: " + tournament_time)
        minutes = tournament['check_in_duration']
        if minutes:
            checkin_time = get_checkin_time(tournament_time, minutes)
            await ctx.send("Checkin Date and Time: " + checkin_time)


@bot.command(name="matches")
async def get_matches(ctx):
    # Get matches
    # Check if the call is in the Tournament Bracket Channel
    if ctx.channel.id in [bracket_id, bot_test_id]:
        matches = challonge_tournament.get_matches(tournament, current_tournament)
        round = 1
        if matches:
            for fighters in matches:
                await ctx.send("Match: " + str(round))
                await ctx.send(fighters[0] + " as" + fighters[1] + " VS " + fighters[2] + " as " + fighters[3])
                if len(fighters) == 3:
                    await ctx.send("Winner: " + fighters[4])
                if len(matches) >= round:
                    round = len(matches)
                else:
                    round += 1
        else:
            await ctx.send("Tournament Has Not Started!!")
            await ctx.send("Start Date and Time: " + tournament_time)


@bot.command(name="register")
async def register(ctx):
    # Check if the call is in the Maniacs Tournament Channel
    if ctx.channel.id in [main_id, bot_test_id]:
        if tournament['state'] == 'pending':
            register_url = challonge_tournament.register_url(tournament)
            await ctx.send("Register @ " + register_url)
        else:
            await ctx.send("Tournament Has Started!!")
    else:
        print("Not in channel restriction")


# Run the bot
bot.run(TOKEN)