import requests
from models.team import Team
from models.conference import Conference
from models.division import Division
from models.player import Player
from models.game import Game
from models.play import Play
from models.faceoff import Faceoff
from models.shot import Shot
from models import db
import logging
from datetime import datetime
from shapely.geometry import Point

logger = logging.getLogger('population')

TIME_FMT = '%Y-%m-%dT%H:%M:%SZ'


def generate_conference_object(conference_json):
    id = conference_json['id']
    team_conf = db.session.query(Conference)\
        .filter_by(id=id).first()

    if team_conf is None:
        logger.warning(f"conference {conference_json['name']} not found in db. inserting now.")

        team_conf = Conference(
            id=id,
            nhl_link=conference_json['link'],
            name=conference_json['name'],
        )
        db.session.add(team_conf)
    db.session.commit()
    return team_conf


def generate_division_object(division_json):
    id = division_json['id']
    team_div = db.session.query(Division)\
                         .filter_by(id=id).first()

    if team_div is None:
        logger.warning(f"division {division_json['name']} not found in db. inserting now.")
        team_div = Division(
            id=id,
            nhl_link=division_json['link'],
            name=division_json['name'],
            name_short=division_json['nameShort']
        )
        db.session.add(team_div)
    db.session.commit()
    return team_div


def generate_team_object(team_json):
    team_div = generate_division_object(team_json['division'])
    team_conf = generate_conference_object(team_json['conference'])
    team = Team(
            id=team_json['id'],
            conference=team_conf.id,
            division=team_div.id,
            short_name=team_json['shortName'],
            name=team_json['name'],
            tri_code=team_json['triCode'],
            nhl_link=team_json['link'],
            home_site=team_json['officialSiteUrl'],
            abbreviation=team_json['abbreviation']
        )
    db.session.add(team)
    db.session.commit()
    return team


def generate_player_object(player_json):
    player = db.session.query(Player)\
                       .filter_by(id=player_json['id']).first()
    if player is None:
        logger.warning(f"player {player_json['fullName']} not found. inserting now.")
        player = Player(
            id=player_json['id'],
            birth_city=player_json['birthCity'],
            birth_country=player_json['birthCountry'],
            birth_date=datetime.strptime(player_json['birthDate'], '%Y-%m-%d'),
            first_name=player_json['firstName'],
            last_name=player_json['lastName'],
            nhl_link=player_json['link'],
            nationality=player_json['nationality'],
            position_abb=player_json['primaryPosition']['abbreviation'],
            position_type=player_json['primaryPosition']['type'],
            weight=player_json['weight'],
            shoots_catches=player_json["shootsCatches"]
        )
        db.session.add(player)
    return player


def generate_game_object(game_json):
    game = db.session.query(Game)\
                     .filter_by(id=str(game_json['game']['pk'])).first()
    if game is None:
        logger.warning(f"game with id {game_json['game']['pk']} not found. Adding it in.")

        teams = game_json['teams']
        team_objs = {key: generate_team_object(team) for key, team in teams.items()}

        players = game_json['players']
        player_objs = {key: generate_player_object(player) for key, player in players.items()}

        game = Game(
            id=str(game_json['game']['pk']),
            start_time=datetime.strptime(game_json['datetime']['dateTime'], TIME_FMT),
            end_time=datetime.strptime(game_json['datetime']['endDateTime'], TIME_FMT),
            season=game_json['game']['season'],
            venue=game_json['venue']['name'],
            home=team_objs['home'].id,
            away=team_objs['away'].id,
            game_type=game_json['game']['type']
        )
        db.session.add(game)
    db.session.commit()
    return game


def generate_play_object(play_json, game_obj):
    # TODO: check for duplicates before adding in

    play = Play(
        game_id=game_obj.id,
        period_clock=play_json['about']['periodTime'],
        period=play_json['about']['period'],
        period_type=play_json['about']['periodType'],
        description=play_json['result']['description'],
        event_code=play_json['result']['eventCode'],
    )
    if play_json['coordinates'].get('x'):
        play.position = Point([play_json['coordinates']['x'], play_json['coordinates']['y']]).wkt

    play_type = play_json['result']['eventTypeId']

    if play_json.get('players'):
        player_dict = {row['playerType']: row['player']['id'] for row in play_json['players']}
    else:
        player_dict = None

    if play_type == 'FACEOFF':
        faceoff = Faceoff(
            winning_player_id=player_dict['Winner'],
            losing_player_id=player_dict['Loser']
        )
        play.faceoff_id = faceoff.id
        db.session.add(faceoff)

    elif play_type in ['SHOT', 'BLOCKED_SHOT',
                       'MISSED_SHOT', 'GOAL']:

        shot = Shot(
            shot_result=play_json['result']['eventTypeId'],
            secondary_type=play_json['result'].get('secondaryType'),
            blocker_id=player_dict.get('Blocker'),
            goalie_id=player_dict.get('Goalie')
        )
        if play_type == 'GOAL':
            shot.shooter_id = player_dict['Scorer']
            shot.scored = True
        else:
            shot.shooter_id = player_dict['Shooter']
            shot.scored = False
        play.shot_id = shot.id
        db.session.add(shot)
    elif play_type in ['HIT', 'GIVEAWAY',
                       'TAKEAWAY', 'STOP',
                       'PENALTY']:
        # to implement
        return None
    elif play_type in ['GAME_SCHEDULED', 'GAME_END',
                       'PERIOD_END', 'PERIOD_OFFICIAL',
                       'GAME_OFFICIAL', 'PERIOD_READY',
                       'PERIOD_START']:
        # wont implement: these should be derivable from metadata
        return None
    else:
        logger.error(f"play type {play_type} not dealt with in population script")
        raise NotImplementedError
    db.session.add(play)
    db.session.commit()


def input_game_data(game_json):
    game_obj = generate_game_object(game_json['gameData'])
    # pp(game_json.keys())
    plays = [generate_play_object(play_json, game_obj) for play_json in game_json['liveData']['plays']['allPlays']]


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    out = requests.get('http://statsapi.web.nhl.com/api/v1/game/2019020010/feed/live')
    stuff = out.json()
    input_game_data(stuff)
    db.session.commit()
