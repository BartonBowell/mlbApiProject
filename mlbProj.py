import statsapi


def roster(teams, teamNameList):
    """
    Displays the opening day roster for a given team and season.

    Parameters:
    teams (dict): A dictionary containing teams and their opening day rosters.
    teamNameList (dict): A dictionary containing team names and their corresponding keys in the teams dictionary.

    Returns:
    None
    """
    team = input("Input Team Name")
    year = input("Which Season")
    if team in teams: 
        print(teams.get(team))
        print_opening_day_roster(teams.get(team), year)
        roster(teams, teamNameList)
    elif team in teamNameList:
        print(teamNameList.get(team))
        print_opening_day_roster(teamNameList.get(team), year)
        roster(teams, teamNameList)
    else:
        print('Team Not Found')
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
    print(team_id)
    datePog = statsapi.get('season', {'seasonId': int(year), 'sportId': 1})
    print('%s' % statsapi.roster(team_id, 'active', date=statsapi.get('season', {'seasonId': int(year), 'sportId': 1})['seasons'][0]['seasonStartDate']))
    return statsapi.roster(team_id, 'active', date=statsapi.get('season', {'seasonId': int(year), 'sportId': 1})['seasons'][0]['seasonStartDate'])


def search(player_name,year):
    """
    Search for a player by name and display their stats for the 2023 season.
    If the player is a batter, call the search_batter function.
    If the player is a two-way player, call both the search_batter and search_pitcher functions.
    If the player is a pitcher, call the search_pitcher function.
    
    Args:
        player_name (str): The name of the player to search for.
    """
    print(statsapi.lookup_player(player_name, season=2023))
    for player in statsapi.lookup_player(player_name, season=2023):
        if player['primaryPosition']['abbreviation'] != 'P' and player['primaryPosition']['abbreviation'] != 'TWP':
            search_batter(player,year)
        # Two Way Players
        if player['primaryPosition']['abbreviation'] == 'TWP':
            search_batter(player,year)
            search_pitcher(player,year)
        elif player['primaryPosition']['abbreviation'] == 'P':
            search_pitcher(player,year)


def search_pitcher(player,year):
    """
    Search for pitching stats of a given player.

    Parameters:
    player (dict): A dictionary containing player information, including 'id', 'fullFMLName', and 'primaryPosition'.

    Returns:
    None
    """
    playerId=player['id']
    stats = statsapi.get('people', {'personIds': playerId, 'season': year, 'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={year})'})['people'][0]
    if 'stats' in stats:
        for i in range(1, 6):  # Assuming you want to iterate from 1 to 3
            if len(stats['stats']) > i and 'era' in stats['stats'][i]['splits'][0]['stat']:
                print(f"{player['fullFMLName']} ({player['primaryPosition']['abbreviation']})")
                print("Pitching Stats:")
                print(f"  ERA: {stats['stats'][i]['splits'][0]['stat']['era']}  WHIP: {stats['stats'][i]['splits'][0]['stat']['whip']} "
                      f"Win %: {stats['stats'][i]['splits'][0]['stat']['winPercentage']}  BB/9: {stats['stats'][i]['splits'][0]['stat']['walksPer9Inn']} \n"
                      f"  H/9: {stats['stats'][i]['splits'][0]['stat']['hitsPer9Inn']}  HR/9: {stats['stats'][i]['splits'][0]['stat']['homeRunsPer9']} "
                      f"HBP: {stats['stats'][i]['splits'][0]['stat']['hitBatsmen']} \n")
                break  # Break out of the loop once the condition is satisfied
        else:
            print(f"{player['fullFMLName']} Has No MLB Stats\n")


def search_batter(player,year):
    """
    Search for a batter's MLB stats and print them.

    Parameters:
    player (dict): A dictionary containing player information, including 'id', 'fullFMLName', and 'primaryPosition'.

    Returns:
    None
    """
    playerId=player['id']
    stats = statsapi.get('people', {'personIds': playerId, 'season': year, 'hydrate': f'stats(group=[hitting,pitching,fielding],type=season,season={year})'})['people'][0]
    if 'stats' in stats and len(stats['stats']) > 0 and 'avg' in stats['stats'][0]['splits'][0]['stat']:
        print(f"{player['fullFMLName']} ({player['primaryPosition']['abbreviation']})")
        print("Batting Stats:")
        print(f"  AVG: {stats['stats'][0]['splits'][0]['stat']['avg']}  OBP: {stats['stats'][0]['splits'][0]['stat']['obp']} "
              f"SLG: {stats['stats'][0]['splits'][0]['stat']['slg']}  OPS: {stats['stats'][0]['splits'][0]['stat']['ops']} \n"
              f"  Doubles: {stats['stats'][0]['splits'][0]['stat']['doubles']}  Triples: {stats['stats'][0]['splits'][0]['stat']['triples']} "
              f"Home Runs: {stats['stats'][0]['splits'][0]['stat']['homeRuns']} \n")
    else:
        print(f"{player['fullFMLName']} Has No MLB Stats\n")




def main():
    personId = statsapi.lookup_player('Trout')[0]['id']
    tStats = statsapi.get('people', {'personIds': personId, 'season': 2021, 'hydrate': 'stats(group=[hitting,pitching,fielding],type=season,season=2021)'})['people'][0]['stats'][0]['splits'][0]['stat']
    teams = {'Arizona Diamondbacks': 109, 'Atlanta Braves': 144, 'Baltimore Orioles': 110, 'Boston Red Sox': 111, 'Chicago Cubs': 112, 'Chicago White Sox': 145, 'Cincinnati Reds': 113, 'Cleveland Guardians': 114, 'Colorado Rockies': 115, 'Detroit Tigers': 116, 'Houston Astros': 117, 'Kansas City Royals': 118, 'Los Angeles Angels': 108, 'Los Angeles Dodgers': 119, 'Miami Marlins': 146, 'Milwaukee Brewers': 158, 'Minnesota Twins': 142, 'New York Mets': 121, 'New York Yankees': 147, 'Oakland Athletics': 133, 'Philadelphia Phillies': 143, 'Pittsburgh Pirates': 134, 'San Diego Padres': 135, 'San Francisco Giants': 137, 'Seattle Mariners': 136, 'St. Louis Cardinals': 138, 'Tampa Bay Rays': 139, 'Texas Rangers': 140, 'Toronto Blue Jays': 141, 'Washington Nationals': 120}
    teamNameList = {'Angels': 108, 'Astros': 117, 'Athletics': 133, 'Blue Jays': 141, 'Braves': 144, 'Brewers': 158, 'Cardinals': 138, 'Cubs': 112, 'Diamondbacks': 109, 'Dodgers': 119, 'Giants': 137, 'Indians': 114, 'Mariners': 136, 'Marlins': 146, 'Mets': 121, 'Nationals': 120, 'Orioles': 110, 'Padres': 135, 'Phillies': 143, 'Pirates': 134, 'Rangers': 140, 'Rays': 139, 'Red Sox': 111, 'Reds': 113, 'Rockies': 115, 'Royals': 118, 'Tigers': 116, 'Twins': 142, 'White Sox': 145, 'Yankees': 147, 'LAA': 108, 'HOU': 117, 'OAK': 133, 'TOR': 141, 'ATL': 144, 'MIL': 158, 'STL': 138, 'CHC': 112, 'ARI': 109, 'LAD': 119, 'SF': 137, 'CLE': 114, 'SEA': 136, 'MIA': 146, 'NYM': 121, 'WSH': 120, 'BAL': 110, 'SD': 135, 'PHI': 143, 'PIT': 134, 'TEX': 140, 'TB': 139, 'BOS': 111, 'CIN': 113, 'COL': 115, 'KC': 118, 'DET': 116, 'MIN': 142, 'CWS': 145, 'NYY': 147}
    print('Which Command Would you like to use?')
    print('Search: Search for a players stats.\nRoster:Display opening day roster for a team: ')
    command = input()
    if command == 'Search' or command =='search':
        player_name = input("Input Player First, Middle, or Last Name of any player currently on the 40-man Roster: ")
        year = input("Which Season: ")
        search(player_name,year)
    elif command == 'Roster' or command == 'roster':
        roster(teams, teamNameList)


if __name__ == "__main__":
    main()
