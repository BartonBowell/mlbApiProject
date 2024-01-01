import statsapi
import pprint


def roster(teams, teamNameList):
    """
    Displays the opening day roster for a given team and season.

    Parameters:
    teams (dict): A dictionary containing teams and their opening day rosters.
    teamNameList (dict): A dictionary containing team names and their corresponding keys in the teams dictionary.

    Returns:
    None
    """
    team = input("Input Team Name:\n").lower()
    year = input("Which Season:\n").lower()
    if team in teams: 
        print_opening_day_roster(teams.get(team), year)
        main()
    elif team in teamNameList:
        print_opening_day_roster(teamNameList.get(team), year)
        main()
    else:
        print('Team Not Found')
        main()

def compare(player1, player2, year):
    """
    Compare the stats of two players for a given season.

    Parameters:
    player1 (dict): A dictionary containing player information, including 'id', 'fullFMLName', and 'primaryPosition'.
    player2 (dict): A dictionary containing player information, including 'id', 'fullFMLName', and 'primaryPosition'.
    year (int): The year of the season.

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
        print(f"{id_1[0]['fullFMLName']} Stats:")
        print_batter_stats(stats1)
        print(f"{id_2[0]['fullFMLName']} Stats:")
        print_batter_stats(stats2)
        main()
    else:
        print(f"{player1['fullFMLName']} Has No MLB Stats")
        main()

def print_opening_day_roster(team_id, year):
    """
    Prints the opening day roster for a given team and year.

    Parameters:
    team_id (int): The ID of the team.
    year (int): The year of the season.

    Returns:
    None
    """
    datePog = statsapi.get('season', {'seasonId': int(year), 'sportId': 1})
    roster = statsapi.roster(team_id, 'active', date=statsapi.get('season', {'seasonId': int(year), 'sportId': 1})['seasons'][0]['seasonStartDate'])
    print(f"Opening Day Roster for Team ID {team_id} in {year}:")
    for player in roster:
        print(f"Player: {player['person']['fullName']}, Position: {player['position']['abbreviation']}", end=", ")
    print()
    main()


def search(player_name, year):
    """
    Search for a player by name and display their stats for the given season.
    If the player is a batter, call the search_batter function.
    If the player is a two-way player, call both the search_batter and search_pitcher functions.
    If the player is a pitcher, call the search_pitcher function.
    
    Args:
        player_name (str): The name of the player to search for.
        year (int): The year of the season.
    """
    for player in statsapi.lookup_player(player_name, season=year):
        if player['primaryPosition']['abbreviation'] != 'P' and player['primaryPosition']['abbreviation'] != 'TWP':
            search_batter(player, year)
        # Two Way Players
        if player['primaryPosition']['abbreviation'] == 'TWP':
            search_batter(player, year)
            search_pitcher(player, year)
        elif player['primaryPosition']['abbreviation'] == 'P':
            search_pitcher(player, year)


def search_pitcher(player, year):
    """
    Search for pitching stats of a given player.

    Parameters:
    player (dict): A dictionary containing player information, including 'id', 'fullFMLName', and 'primaryPosition'.
    year (int): The year of the season.

    Returns:
    None
    """
    playerId = player['id']
    stats = statsapi.get('people', {'personIds': playerId, 'season': year, 'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={year})'})['people'][0]
    if 'stats' in stats:
        for i in range(1, 6):  # Assuming you want to iterate from 1 to 5
            if len(stats['stats']) > i and 'era' in stats['stats'][i]['splits'][0]['stat']:
                print_pitcher_stats(stats,i)
                main()
        else:
            print(f"{player['fullFMLName']} Has No MLB Stats")
            main()

def print_pitcher_stats(stats,i):
    """
    Prints the pitching stats of a given player.

    Parameters:
    stats (dict): A dictionary containing the stats of a player.

    Returns:
    stats (dict): A dictionary containing the stats of a player.
    """

    stats_list = [
    "Pitching Stats:",
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
    print('\n'.join(stats_list))
    return stats_list

def print_batter_stats(stats):
    """
    Prints the batting stats of a given player.

    Parameters:
    stats (dict): A dictionary containing the stats of a player.

    Returns:
    None
    """
    stats_list = [
    "Batting Stats:",
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

    print('\n'.join(stats_list))
    return stats_list

def search_batter(player, year):
    """
    Search for a batter's MLB stats and print them.

    Parameters:
    player (dict): A dictionary containing player information, including 'id', 'fullFMLName', and 'primaryPosition'.
    year (int): The year of the season.

    Returns:
    None
    """
    playerId = player['id']
    stats = statsapi.get('people', {'personIds': playerId, 'season': year, 'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={year})'})['people'][0]
    if 'stats' in stats and len(stats['stats']) > 0 and 'avg' in stats['stats'][0]['splits'][0]['stat']:
        print_batter_stats(stats)
        main()
    else:
        print(f"{player['fullFMLName']} Has No MLB Stats")
        main()


def main():
    teams = {'arizona diamondbacks': 109, 'atlanta braves': 144, 'baltimore orioles': 110, 'boston red sox': 111, 'chicago cubs': 112, 'chicago white sox': 145, 'cincinnati reds': 113, 'cleveland guardians': 114, 'colorado rockies': 115, 'detroit tigers': 116, 'houston astros': 117, 'kansas city royals': 118, 'los angeles angels': 108, 'los angeles dodgers': 119, 'miami marlins': 146, 'milwaukee brewers': 158, 'minnesota twins': 142, 'new york mets': 121, 'new york yankees': 147, 'oakland athletics': 133, 'philadelphia phillies': 143, 'pittsburgh pirates': 134, 'san diego padres': 135, 'san francisco giants': 137, 'seattle mariners': 136, 'st. louis cardinals': 138, 'tampa bay rays': 139, 'texas rangers': 140, 'toronto blue jays': 141, 'washington nationals': 120}
    teamNameList = {'angels': 108, 'astros': 117, 'athletics': 133, 'blue jays': 141, 'braves': 144, 'brewers': 158, 'cardinals': 138, 'cubs': 112, 'diamondbacks': 109, 'dodgers': 119, 'giants': 137, 'guardians': 114, 'mariners': 136, 'marlins': 146, 'mets': 121, 'nationals': 120, 'orioles': 110, 'padres': 135, 'phillies': 143, 'pirates': 134, 'rangers': 140, 'rays': 139, 'red sox': 111, 'reds': 113, 'rockies': 115, 'royals': 118, 'tigers': 116, 'twins': 142, 'white sox': 145, 'yankees': 147, 'laa': 108, 'hou': 117, 'oak': 133, 'tor': 141, 'atl': 144, 'mil': 158, 'stl': 138, 'chc': 112, 'ari': 109, 'lad': 119, 'sf': 137, 'cle': 114, 'sea': 136, 'mia': 146, 'nym': 121, 'wsh': 120, 'bal': 110, 'sd': 135, 'phi': 143, 'pit': 134, 'tex': 140, 'tb': 139, 'bos': 111, 'cin': 113, 'col': 115, 'kc': 118, 'det': 116, 'min': 142, 'cws': 145, 'nyy': 147}
    print('Which Command Would you like to use?')
    print('Search: Search for a player\'s stats.\nRoster: Display opening day roster for a team.')
    command = input()
    if command.lower() == 'search':
        player_name = input("Input Player First, Middle, or Last Name of any player currently on the 40-man Roster: ")
        year = input("Which Season: ")
        search(player_name, year)
    elif command.lower() == 'roster':
        roster(teams, teamNameList)
    elif command.lower() == 'compare':
        playerOne = input('Input Player One')
        playerTwo = input('Input Player Two')
        year = input('Which Season')
        compare(playerOne, playerTwo, year)


if __name__ == "__main__":
    main()
