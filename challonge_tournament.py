import challonge
import iso8601
import tzlocal
import pytz
import requests

# Custom Library's
from time_conversion import convert_start_time


def set_creds(username, api_key):
    challonge.set_credentials(username, api_key)


def get_tournament(tournament):
    tournament = challonge.tournaments.show(tournament)
    return tournament


def get_matches(tournament, current_tournament):
    participants = challonge.participants.index(tournament["id"])
    matches = challonge.matches.index(current_tournament)
    player_pairs = []
    for match in matches:
        player1 = None
        player2 = None
        fighter1 = None
        fighter2 = None
        winner = None

        for player in participants:
            if player['id'] == match['player1_id']:
                player1 = player['display_name']
                fighter1 = player['challonge_username']
            if player['id'] == match['player2_id']:
                player2 = player['display_name']
                fighter2 = player['challonge_username']
            if player['id'] == match['winner_id']:
                winner = player['display_name']

        # Once player1 and player2 are found, append to the player_pairs list
        if player1 and player2 and winner:
            player_pairs.append([player1, fighter1, player2, fighter2, winner])
        elif player1 and player2:
            player_pairs.append([player1, player2])
    # print("Matches: ", matches)
    # print("Participants: ", participants)
    return player_pairs


def get_participants(tournament):
    # Retrieve the participants for a given tournament.
    participants = challonge.participants.index(tournament["id"])
    usernames = [[player['challonge_username'], 'TBA' if player['challonge_username'] == player['display_name'] else player['display_name']] for player in participants]
    return usernames


def tournament_name(tournament):
    return tournament["name"]


def tournament_start_time(tournament):
    # Receive the Start Time of Event
    check_in_time = tournament["started_checking_in_at"]
    return convert_start_time(str(tournament["start_at"])) # 2011-07-31 16:16:02-04:00


def register_url(tournament):
    return tournament['sign_up_url']