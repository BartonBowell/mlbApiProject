import statsapi
import pprint
import datetime


#Fix Later, do current year - One during off season dates
today = datetime.date.today()
current_year = today.year()
def r(teams, teamNameList):
        team = input("Input Team Name")
        year = input("Which Season")
        if team in teams: 
            print(teams.get(team))
            print_opening_day_roster(teams.get(team),year)
            r(teams, teamNameList)
        elif team in teamNameList:
            print(teamNameList.get(team))
            print_opening_day_roster(teamNameList.get(team),year)
            r(teams, teamNameList)
        else:
            print('Team Not Found')
            main()
def print_opening_day_roster(team_id,year):
    print(team_id)
    #team_id = statsapi.lookup_team(team_name)
    #print(team_id['id'])
    datePog=statsapi.get('season',{'seasonId':int(year),'sportId':1})
    print('%s' % statsapi.roster(team_id,'active',date=statsapi.get('season',{'seasonId':int(year),'sportId':1})['seasons'][0]['seasonStartDate']))
    print('g')


def search(player_name):
     print(statsapi.lookup_player(player_name,season = current_year))
     for player in statsapi.lookup_player(player_name,season = current_year):
            if player['primaryPosition']['abbreviation'] != 'P' and player['primaryPosition']['abbreviation'] != 'TWP':
                search_batter(player)
            #Two Way Players
            if player['primaryPosition']['abbreviation'] == 'TWP':
                search_batter(player)
                search_pitcher(player)
            else:
                search_pitcher(player)

def search_pitcher(player):
    stats = statsapi.player_stat_data(player['id'], group="[hitting,pitching,fielding]", type="career", sportId=1)
    if 'stats' in stats:
        for i in range(1, 6):  # Assuming you want to iterate from 1 to 3
            if len(stats['stats']) > i and 'era' in stats['stats'][i]['stats']:
                print(f"{player['fullFMLName']} ({player['primaryPosition']['abbreviation']}) of the {stats['current_team']}")
                print("Pitching Stats:")
                print(f"  ERA: {stats['stats'][i]['stats']['era']}  WHIP: {stats['stats'][i]['stats']['whip']} "
                      f"Win %: {stats['stats'][i]['stats']['winPercentage']}  BB/9: {stats['stats'][i]['stats']['walksPer9Inn']} \n"
                      f"  H/9: {stats['stats'][i]['stats']['hitsPer9Inn']}  HR/9: {stats['stats'][i]['stats']['homeRunsPer9']} "
                      f"HBP: {stats['stats'][i]['stats']['hitBatsmen']} \n")
                break  # Break out of the loop once the condition is satisfied
        else:
            print(f"{player['fullFMLName']} Has No MLB Stats\n")

def search_batter(player):
    stats = statsapi.player_stat_data(player['id'], group="[hitting,pitching,fielding]", type="career", sportId=1)
    if 'stats' in stats and len(stats['stats']) > 0 and 'avg' in stats['stats'][0]['stats']:
        print(f"{player['fullFMLName']} ({player['primaryPosition']['abbreviation']}) of the {stats['current_team']}")
        print("Batting Stats:")
        print(f"  AVG: {stats['stats'][0]['stats']['avg']}  OBP: {stats['stats'][0]['stats']['obp']} "
              f"SLG: {stats['stats'][0]['stats']['slg']}  OPS: {stats['stats'][0]['stats']['ops']} \n"
              f"  Doubles: {stats['stats'][0]['stats']['doubles']}  Triples: {stats['stats'][0]['stats']['triples']} "
              f"Home Runs: {stats['stats'][0]['stats']['homeRuns']} \n")
    else:
        print(f"{player['fullFMLName']} Has No MLB Stats\n")

def main():
    teams = {}
    teamNameList = {}
    for x in statsapi.get('teams',{'sportIds':1,'activeStatus':'Yes','fields':'teams,name'})['teams']:
        teamid = statsapi.lookup_team(x['name'])
        teams.update({x['name']:teamid[0]['id']})
        teamNameList.update({teamid[0]['teamName']:teamid[0]['id']})
    pprint.pprint(teams)
    pprint.pprint(teamNameList)
    command = input('Which Command Would you like to use?\n Search: Search for a players stats.\nRoster:Display opening day roster for a team')
    if command == 'Search' or command =='search':
        player_name = input("Input Player First, Middle, or Last Name of any player currently on the 40-man Roster: ")
        search(player_name)
    elif command == 'Roster' or command == 'roster':
        r(teams,teamNameList)

    #print('Phillies 40-man roster on opening day of the 2018 season:\n%s' % statsapi.roster(143,'40Man',date=statsapi.get('season',{'seasonId':2018,'sportId':1})['seasons'][0]['regularSeasonStartDate']))

  

if __name__ == "__main__":
    main()
