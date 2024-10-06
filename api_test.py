import os
from dotenv import load_dotenv

# Custom Library's
import challonge_tournament


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

# tests
challonge_tournament.get_all_tournaments()
print(challonge_tournament.get_tournament(current_tournament))