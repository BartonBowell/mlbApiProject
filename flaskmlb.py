from flask import Flask, render_template, request
import mlbapi

app = Flask(__name__)

@app.route('/roster', methods=['GET', 'POST'])
def roster():
    if request.method == 'POST':
        team = request.form.get('team').lower()
        year = int(request.form.get('year'))
        roster = mlbapi.roster(team, year).split('\n')
        print(roster)
        print(type(roster))
    else:
        roster = []
    return render_template('index.html', roster=roster)

@app.route('/search', methods=['GET', 'POST'])
def search():
    player_stats = []
    if request.method == 'POST':
        player = request.form.get('player')
        year = int(request.form.get('year'))
        player_stats = mlbapi.search(player, year)
        
        print(player_stats)
        print(type(player_stats))
    else:
        search = []
    return render_template('search.html', search=player_stats)

if __name__ == "__main__":
    app.run(debug=True)