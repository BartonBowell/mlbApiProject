from flask import Flask, render_template, request
import mlbProj

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/roster', methods=['GET', 'POST'])
def roster():
    if request.method == 'POST':
        team = request.form.get('team').lower()
        year = request.form.get('year')
        roster = mlbProj.roster(team, year).split('\n')
    else:
        roster = []
    return render_template('roster.html', roster=roster)

@app.route('/matchup', methods=['GET', 'POST'])
def matchup():
    if request.method == 'POST':
        player_one = request.form.get('player_one')
        player_two = request.form.get('player_two')
        year = int(request.form.get('year'))
        matchup = mlbProj.matchup(player_one, player_two, year)
    else:
        matchup = []
    return render_template('matchup.html', matchup=matchup)

@app.route('/search', methods=['GET', 'POST'])
def search():
 
    player_stats = []
    if request.method == 'POST':
        player = request.form.get('player')
        year = request.form.get('year')
        player_stats = mlbProj.search(player, (year))
        print(type(player_stats[0]))
    else:
        player_stats = []
    return render_template('search.html', search=player_stats)

@app.route('/boxscore', methods=['GET', 'POST'])
def get_box_score():
    if request.method == 'POST':
        game_id = request.form.get('game_id')
        team_one = request.form.get('team_one')
        team_two = request.form.get('team_two')
        date = request.form.get('date')
        box_score = mlbProj.get_box_score(game_id,team_one,team_two)
        print(box_score)
    else:
        box_score = []
    return render_template('boxscore.html', box_score=box_score)

@app.route('/gameid', methods=['GET', 'POST'])
def game_id():
    game_id = ''
    if request.method == 'POST':
        team_one = request.form.get('team_one')
        team_two = request.form.get('team_two')
        year = request.form.get('date')
        game_id = mlbProj.get_game_ids(team_one,team_two,year)
    else:
        game_id = []
    if len(game_id) >= 2:  # Check if 'game_id' has at least two elements
        return render_template('gameid.html', game_id=game_id[0], dates=game_id[1])
    else:
        return render_template('gameid.html', game_id=None, dates=None)  # Return default values if 'game_id' has less than two elements


if __name__ == "__main__":
    app.run(debug=True)