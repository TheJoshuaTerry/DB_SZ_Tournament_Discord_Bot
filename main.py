import asyncio
import os
import discord
from discord.ext import commands
# from discord.ext.commands import cooldown
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

# Custom Library's
import challonge_tournament
from time_conversion import get_checkin_time

# Get Information for .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
API_Key = os.getenv('API_V1')
USERNAME = os.getenv('CHALLONGE_USERNAME')
current_tournament = os.getenv('CURRENT_TOURNAMENT')
bot_test_id = int(os.getenv('BOT_TEST')) # Test Channel
main_id = int(os.getenv('MAIN')) # Sparking Zero
bracket_id = int(os.getenv('BRACKET')) # Tournament Bracket
char_select_id = int(os.getenv('CHARACTER_SELECT')) # Character Select
tournament_id = int(os.getenv('TOURNAMENT')) # Maniacs Tournament

# Cooldown rate variables
cooldown_rate = 1 # Times called before cooldown
cooldown_time = 120 # In seconds

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
    await countdown()

# Command that the bot will respond to with "Pong!"
@bot.command(name="fighters")
@commands.cooldown(cooldown_rate, cooldown_time, commands.BucketType.user)
async def _fighters(ctx):
    # Get Participants and Chosen Fighters
    # Check if the call is in the Character Select Channel
    if ctx.channel.id in [char_select_id, bot_test_id]:
        players_fighters = challonge_tournament.get_participants(tournament)
        for player_fighter in players_fighters:
            await ctx.send(player_fighter[0] + " as " + player_fighter[1])


# Command that the bot will respond to with "Pong!"
@bot.command(name="players")
@commands.cooldown(cooldown_rate, cooldown_time, commands.BucketType.user)
async def _players(ctx):
    # Get Participants
    # Check if the call is in the Maniacs Tournament and Tournament Bracket Channels
    if ctx.channel.id in [tournament_id, bracket_id, bot_test_id]:
        players = challonge_tournament.get_participants(tournament)
        for player in players:
            await ctx.send(player[0])


@bot.command(name="begin")
@commands.cooldown(cooldown_rate, cooldown_time, commands.BucketType.user)
async def _begin(ctx):
    # Check if the call is in the Maniacs Tournament Channel
    if ctx.channel.id in [tournament_id, bot_test_id]:
        await ctx.send("Tournament: " + tournament_name)
        await ctx.send("Start Date and Time: " + tournament_time)
        minutes = tournament['check_in_duration']
        if minutes:
            checkin_time = get_checkin_time(tournament_time, minutes)
            await ctx.send("Checkin Date and Time: " + checkin_time)


@bot.command(name="matches")
@commands.cooldown(cooldown_rate, cooldown_time, commands.BucketType.user)
async def _get_matches(ctx):
    # Get matches
    # Check if the call is in the Tournament Bracket Channel
    if ctx.channel.id in [bracket_id, bot_test_id]:
        matches = challonge_tournament.get_matches(tournament, current_tournament)
        round = 1
        if matches:
            for fighter in matches:
                await ctx.send("Match: " + str(round))
                await ctx.send(fighter[0] + " as" + fighter[1] + " VS " + fighter[2] + " as " + fighter[3])
                if len(fighter) == 3:
                    await ctx.send("Winner: " + fighter[4])
                round += 1
        else:
            await ctx.send("Tournament Has Not Started!!")
            await ctx.send("Start Date and Time: " + tournament_time)


@bot.command(name="register")
@commands.cooldown(cooldown_rate, cooldown_time, commands.BucketType.user)
async def _register(ctx):
    # Check if the call is in the Maniacs Tournament Channel
    if ctx.channel.id in [tournament_id, bot_test_id]:
        if tournament['state'] == 'pending':
            register_url = challonge_tournament.register_url(tournament)
            await ctx.send("Register @ " + register_url)
        else:
            await ctx.send("Tournament Has Started!!")
    else:
        print("Not in channel restriction")


async def countdown():
    channel = bot.get_channel(bot_test_id)

    start_time = datetime(2024, 10, 12,15 , 0, 0, tzinfo=pytz.timezone('US/Central'))
    check_in_time = datetime(2024, 10, 12, 13, 0, 0, tzinfo=pytz.timezone('US/Central'))

    countdown_prefix = "Tournament"

    while True:
        now = datetime.now(pytz.timezone('US/Central'))
        remaining_time = start_time - now
        remaining_time_till_check_in = check_in_time - now

        if remaining_time_till_check_in.total_seconds() > 3600 * 2:
            message_suffix = f"\nCheck-In starts 2 hours before the tournament begins!!!!!"
        else:
            message_suffix = f"\nCheck-In has began. Get checked in before the tournament starts.\nFailure to check in could result in a disqualification!!!!"


        if remaining_time.total_seconds() <= 0:
            await channel.send("Countdown finished!\nThe Tournament STARTS NOW!!!!")
            break
        else:
            days = remaining_time.days
            hours, remainder = divmod(remaining_time.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            if days > 1:
                countdown_message = f"Time remaining until {countdown_prefix}: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
            elif days == 1:
                countdown_message = f"Time remaining until {countdown_prefix}: {days} day, {hours} hours, {minutes} minutes, {seconds} seconds"
            else:
                countdown_message = f"Time remaining until {countdown_prefix}: {hours} hours, {minutes} minutes, {seconds} seconds"

            countdown_message = countdown_message + message_suffix

            await channel.send(countdown_message)

            if remaining_time.total_seconds() < 15:
                await asyncio.sleep(1)
            elif remaining_time.total_seconds() < 60:
                await asyncio.sleep(15)
            elif remaining_time.total_seconds() < 3600:
                await asyncio.sleep(300)
            elif remaining_time.total_seconds() < 7200:
                await asyncio.sleep(900)
            elif remaining_time.total_seconds() < 24 * 3600:
                await asyncio.sleep(3600)
            else:
                await asyncio.sleep(2 * 3600)


# Run the bot
bot.run(TOKEN)