import statsapi

teams = {'arizona diamondbacks': 109, 'atlanta braves': 144, 'baltimore orioles': 110, 'boston red sox': 111, 'chicago cubs': 112, 'chicago white sox': 145, 'cincinnati reds': 113, 'cleveland guardians': 114, 'colorado rockies': 115, 'detroit tigers': 116, 'houston astros': 117, 'kansas city royals': 118, 'los angeles angels': 108, 'los angeles dodgers': 119, 'miami marlins': 146, 'milwaukee brewers': 158, 'minnesota twins': 142, 'new york mets': 121, 'new york yankees': 147, 'oakland athletics': 133, 'philadelphia phillies': 143, 'pittsburgh pirates': 134, 'san diego padres': 135, 'san francisco giants': 137, 'seattle mariners': 136, 'st. louis cardinals': 138, 'tampa bay rays': 139, 'texas rangers': 140, 'toronto blue jays': 141, 'washington nationals': 120,'angels': 108, 'astros': 117, 'athletics': 133, 'blue jays': 141, 'braves': 144, 'brewers': 158, 'cardinals': 138, 'cubs': 112, 'diamondbacks': 109, 'dodgers': 119, 'giants': 137, 'guardians': 114, 'mariners': 136, 'marlins': 146, 'mets': 121, 'nationals': 120, 'orioles': 110, 'padres': 135, 'phillies': 143, 'pirates': 134, 'rangers': 140, 'rays': 139, 'red sox': 111, 'reds': 113, 'rockies': 115, 'royals': 118, 'tigers': 116, 'twins': 142, 'white sox': 145, 'yankees': 147, 'laa': 108, 'hou': 117, 'oak': 133, 'tor': 141, 'atl': 144, 'mil': 158, 'stl': 138, 'chc': 112, 'ari': 109, 'lad': 119, 'sf': 137, 'cle': 114, 'sea': 136, 'mia': 146, 'nym': 121, 'wsh': 120, 'bal': 110, 'sd': 135, 'phi': 143, 'pit': 134, 'tex': 140, 'tb': 139, 'bos': 111, 'cin': 113, 'col': 115, 'kc': 118, 'det': 116, 'min': 142, 'cws': 145, 'nyy': 147}

def roster(team, year):
    """
    Prints the opening day roster for a given team and year.

    Parameters:
    team (str): The name of the team.
    year (int): The year of the roster.

    Returns:
    None
    """
    if team in teams: 
        return opening_day_roster(teams.get(team), year)
    else:
        return('Team Not Found')

def compare(player1, player2, year):
    """
    Compare the stats of two players for a given year.

    Parameters:
    player1 (str): The name of the first player.
    player2 (str): The name of the second player.
    year (int): The year for which to compare the stats.

    Returns:
    None
    """
    id_1 = statsapi.lookup_player(player1, season=year)
    id_2 = statsapi.lookup_player(player2, season=year)
    playerId1 = id_1[0]['id']
    playerId2 = id_2[0]['id']
    stats1 = statsapi.get('people', {'personIds': playerId1, 'season': year, 'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={year})'})['people'][0]
    stats2 = statsapi.get('people', {'personIds': playerId2, 'season': year, 'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={year})'})['people'][0]
    if 'stats' in stats1 and len(stats1['stats']) > 0 and 'avg' in stats1['stats'][0]['splits'][0]['stat']:
        return [batter_stats(stats1), batter_stats(stats2)]

    else:
        return(f"{player1['fullFMLName']} Has No MLB Stats")

def opening_day_roster(team_id, year):
    """
    Prints the opening day roster for a given team ID and year.

    Parameters:
    team_id (int): The ID of the team.
    year (int): The year of the season.

    Returns:
    None
    """
    roster = statsapi.roster(team_id,  season=year)
    return roster


def search(player_name, year):
    """
    Search for a player's statistics based on their name and the specified year.

    Parameters:
    player_name (str): The name of the player.
    year (int): The year of the statistics.

    Returns:
    None
    """
    stat_list = []
    if player_name == '' or year == '':
        return('Invalid Input')
    players = statsapi.lookup_player(player_name, season=year)
    if not players:
        return [['No player found']]
    for player in players:
        if player['primaryPosition']['abbreviation'] != 'P' and player['primaryPosition']['abbreviation'] != 'TWP':
            stat_list.append(search_batter(player, year))
        if player['primaryPosition']['abbreviation'] == 'TWP':
            stat_list.append(search_batter(player, year))
            stat_list.append(search_pitcher(player, year))
        elif player['primaryPosition']['abbreviation'] == 'P':
            stat_list.append(search_pitcher(player, year))
    return stat_list

def search_pitcher(player, year):
    """
    Search for pitcher stats for a given player and year.

    Parameters:
    player (dict): A dictionary containing player information.
    year (int): The year for which to retrieve the stats.

    Returns:
    stats_list (list): A list of formatted pitching statistics.
    """
    playerId = player['id']
    stats = statsapi.get('people', {'personIds': playerId, 'season': year, 'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={year})'})['people'][0]
    if 'stats' in stats:
        for i in range(1, 6):
            if len(stats['stats']) > i and 'era' in stats['stats'][i]['splits'][0]['stat']:
                stat_list = pitcher_stats(stats,i)
                playerName = player['fullFMLName']
                return [stat_list,playerName]
        else:
            return (f"{player['fullFMLName']} Has No MLB Stats")

def pitcher_stats(stats, i):
    """
    Print the pitching statistics for a specific pitcher.

    Args:
        stats (dict): The dictionary containing the pitching statistics.
        i (int): The index of the pitcher in the stats dictionary.

    Returns:
        stat_list: The list of formatted pitching statistics.

    """
    stats_list = [
        f"  ERA: {stats['stats'][i]['splits'][0]['stat']['era']}",
        f"  WHIP: {stats['stats'][i]['splits'][0]['stat']['whip']}",
        f"  Win %: {stats['stats'][i]['splits'][0]['stat']['winPercentage']}",
        f"  BB/9: {stats['stats'][i]['splits'][0]['stat']['walksPer9Inn']}",
        f"  H/9: {stats['stats'][i]['splits'][0]['stat']['hitsPer9Inn']}",
        f"  HR/9: {stats['stats'][i]['splits'][0]['stat']['homeRunsPer9']}",
        f"  Games Played: {stats['stats'][i]['splits'][0]['stat']['gamesPlayed']}",
        f"  HR Allowed: {stats['stats'][i]['splits'][0]['stat']['homeRuns']}",
        f"  Walks: {stats['stats'][i]['splits'][0]['stat']['baseOnBalls']}",
        f"  AVG: {stats['stats'][i]['splits'][0]['stat']['avg']}",
        f"  Saves: {stats['stats'][i]['splits'][0]['stat']['saves']}",
        f"  Blown Saves: {stats['stats'][i]['splits'][0]['stat']['blownSaves']}",
        f"  Holds: {stats['stats'][i]['splits'][0]['stat']['holds']}",
        f"  K/9: {stats['stats'][i]['splits'][0]['stat']['strikeoutsPer9Inn']}",
        f"  K/BB: {stats['stats'][i]['splits'][0]['stat']['strikeoutWalkRatio']}",
        f"  K: {stats['stats'][i]['splits'][0]['stat']['strikeOuts']}",
        f"  IP: {stats['stats'][i]['splits'][0]['stat']['inningsPitched']}"
    ]
    return stats_list


def batter_stats(stats):
    """
    Prints the batting statistics of a player.

    Args:
        stats (dict): A dictionary containing the player's batting statistics.

    Returns:
        list: A list of strings representing the batting statistics.
    """
    if stats == {}:
        print("No Stats Found")
    else:
        stats_list = [
        f"  Position: {stats['primaryPosition']['name']}",
        f"  Games: {stats['stats'][0]['splits'][0]['stat']['gamesPlayed']}",
        f"  AVG: {stats['stats'][0]['splits'][0]['stat']['avg']}",
        f"  OBP: {stats['stats'][0]['splits'][0]['stat']['obp']}",
        f"  SLG: {stats['stats'][0]['splits'][0]['stat']['slg']}",
        f"  OPS: {stats['stats'][0]['splits'][0]['stat']['ops']}",
        f"  Doubles: {stats['stats'][0]['splits'][0]['stat']['doubles']}",
        f"  Triples: {stats['stats'][0]['splits'][0]['stat']['triples']}",
        f"  Home Runs: {stats['stats'][0]['splits'][0]['stat']['homeRuns']}",
        f"  RBI: {stats['stats'][0]['splits'][0]['stat']['rbi']}",
        f"  BABIP: {stats['stats'][0]['splits'][0]['stat']['babip']}",
        f"  AB/HR: {stats['stats'][0]['splits'][0]['stat']['atBatsPerHomeRun']}",
        f"  GIDP: {stats['stats'][0]['splits'][0]['stat']['groundIntoDoublePlay']}",
        f"  PA: {stats['stats'][0]['splits'][0]['stat']['plateAppearances']}",
        f"  SB: {stats['stats'][0]['splits'][0]['stat']['stolenBases']}",
        f"  Walks: {stats['stats'][0]['splits'][0]['stat']['baseOnBalls']}"
        ]
        return stats_list

def search_batter(player, year):
    """
    Search for batter stats for a given player and year.

    Parameters:
    player (dict): A dictionary containing player information.
    year (int): The year for which to retrieve the stats.

    Returns:
    stats_list (list): A list of formatted batting statistics.
    """
    playerId = player['id']
    stats = statsapi.get('people', {'personIds': playerId, 'season': year, 'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={year})'})['people'][0]
    if 'stats' in stats and len(stats['stats']) > 0 and 'avg' in stats['stats'][0]['splits'][0]['stat']:
        stat_list = batter_stats(stats)
        playerName = player['fullFMLName']
        return [stat_list,playerName]
    else:
        return (f"{player['fullFMLName']} Has No MLB Stats")


def get_stat_leader(category, year, type):
    """
    Retrieves the statistical leaders for a given category, year, and type.

    Parameters:
    - category (str): The category of statistics to retrieve.
    - year (int): The year for which to retrieve the statistics.
    - type (str): The type of statistics to retrieve.

    Returns:
    None
    """
    if category == '' or year == '' or type == '':
        return('Invalid Input')
    stat_leaders = []
    stat_leaders_name = []
    response = statsapi.get('stats_leaders', {
        'leaderCategories': category,
        'hydrate': type,
        'sportId': 1,
        'season': year,
        'limit': 25
    })
    for i in range(0, 25): 
        inc = ("{:02d}".format(i))
        stat_leaders.append(response['leagueLeaders'][0]['leaders'][int(inc)]['value'])
        stat_leaders_name.append(response['leagueLeaders'][0]['leaders'][int(inc)]['person']['fullName'])
    stat = response['leagueLeaders'][0]['leaderCategory']
    return [stat_leaders, stat_leaders_name,stat]
        
        
def get_game_id(team_one,team_two,date):
    """
    Retrieves the game IDs for a given team ID and year.

    Parameters:
    - team_id (int): The ID of the team.
    - year (int): The year of the season.

    Returns:
    None
    """
    game_id = statsapi.schedule(date = date,team=teams[team_one],opponent=teams[team_two])
    return [game_id]

def get_game_ids(team_one,team_two,year):
   
    game_ids = []
    game_dates = []
    if team_one != '' or team_two != '' or year != '':
        games = statsapi.schedule(start_date = '5/20/'+str(year),end_date = '12/30/'+str(year),team=teams[team_one],opponent=teams[team_two])
        for game in games:
            game_ids.append(games[games.index(game)]['game_id'])
            game_dates.append(games[games.index(game)]['game_date'])
        return [game_ids,game_dates]
    else:
        return('Invalid Input')

def get_game_data(team_one,team_two, year):
    games = statsapi.schedule(start_date='03/28/'+year,end_date='12/31/'+year,team=teams[team_one],opponent=teams[team_two])
    game_data = []
    for game in games:

        game_data.append(game['game_date'])
    return game_data

'''def get_box_score(homeTeam,awayTeam,year):
    if homeTeam not in teams or awayTeam not in teams:
        return('Invalid Team')
    game_ids = get_game_ids(homeTeam,awayTeam,year)

    print('There are',len(game_ids),'games between the',homeTeam,'and the',awayTeam,'in',year,
          '\nWhich game would you like to see the box score for?')
    for i in range(0,len(game_ids)):
        print(i,':',game_ids[1][i])
    input_game = int(input())
    box_score = statsapi.boxscore(game_ids[input_game])

    return box_score'''





#FIX THIS, DOESNT ALWAYS RETURN PROPER SEASON

def matchup(playerId, opposingPlayerId, year):
    playerOne = statsapi.lookup_player(playerId, season=year)
    playerTwo = statsapi.lookup_player(opposingPlayerId, season=year)
    stat_list = []
    if playerOne == [] or playerTwo == []:
        return('Invalid Player')
    stats = statsapi.get('people', {'personIds': playerOne[0]['id'], 'season': year, 'hydrate': f'stats(group=[hitting,pitching],type=[vsPlayer],opposingPlayerId={playerTwo[0]['id']},season={year})'})['people'][0]
    for i in range(0, 3):
        for j in range(0, len(stats['stats'][i]['splits'])):
            if stats['stats'][i]['type']['displayName'] == 'vsPlayer':
                for k in range(0, len(stats['stats'][i]['splits'])):
                    if stats['stats'][i]['splits'][k]['season']==str(year):
                        if stats['stats'][i]['group']['displayName']=='hitting':
                            stat_list.append(f"{playerOne[0]['fullFMLName']} vs {playerTwo[0]['fullFMLName']} Stats:")
                            stat_list.append(f"  AVG: {stats['stats'][i]['splits'][0]['stat']['avg']}")
                            stat_list.append(f"  OBP: {stats['stats'][i]['splits'][0]['stat']['obp']}")
                            stat_list.append(f"  SLG: {stats['stats'][i]['splits'][0]['stat']['slg']}")
                            stat_list.append(f"  OPS: {stats['stats'][i]['splits'][0]['stat']['ops']}")
                            stat_list.append(f"  Doubles: {stats['stats'][i]['splits'][0]['stat']['doubles']}")
                            stat_list.append(f"  Triples: {stats['stats'][i]['splits'][0]['stat']['triples']}")
                            stat_list.append(f"  Home Runs: {stats['stats'][i]['splits'][0]['stat']['homeRuns']}")
                            stat_list.append(f"  RBI: {stats['stats'][i]['splits'][0]['stat']['rbi']}")
                            stat_list.append(f"  BABIP: {stats['stats'][i]['splits'][0]['stat']['babip']}")
                            stat_list.append(f"  AB/HR: {stats['stats'][i]['splits'][0]['stat']['atBatsPerHomeRun']}")
                            stat_list.append(f"  GIDP: {stats['stats'][i]['splits'][0]['stat']['groundIntoDoublePlay']}")
                            stat_list.append(f"  PA: {stats['stats'][i]['splits'][0]['stat']['plateAppearances']}")
                            stat_list.append(f"  Walks: {stats['stats'][i]['splits'][0]['stat']['baseOnBalls']}")
                            return stat_list
                        elif stats['stats'][i]['group']['displayName']=='pitching':
                            stat_list.append(f"{playerOne[0]['fullFMLName']} vs {playerTwo[0]['fullFMLName']} Stats:")
                            stat_list.append(f"  Runs Allowed: {stats['stats'][i]['splits'][0]['stat']['rbi']}")
                            stat_list.append(f"  WHIP: {stats['stats'][i]['splits'][0]['stat']['whip']}")
                            stat_list.append(f"  Games Played: {stats['stats'][i]['splits'][0]['stat']['gamesPitched']}")
                            stat_list.append(f"  HR Allowed: {stats['stats'][i]['splits'][0]['stat']['homeRuns']}")
                            stat_list.append(f"  Walks: {stats['stats'][i]['splits'][0]['stat']['baseOnBalls']}")
                            stat_list.append(f"  Hits: {stats['stats'][i]['splits'][0]['stat']['hits']}")
                            stat_list.append(f"  AVG: {stats['stats'][i]['splits'][0]['stat']['avg']}")
                            return stat_list

