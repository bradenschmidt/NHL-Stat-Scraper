## NHL.com Stats Scraper
## Braden Schmidt

# Imports
import requests
import bs4
import time
import pprint


# Functions
def parse_player_cols(cols):
## Takes a list of columns and parses to their stat

    name = cols[1]
    #print('name: ' + name)

    team = cols[2]
    pos = cols[3]
    gp = int(cols[4])

    goals = int(cols[5])
    assists = int(cols[6])
    points = goals + assists
    plus_minus = int(cols[8])
    pims = int(cols[9])

    ppg = int(cols[10])
    ppp = int(cols[11])
    ppa = ppp - ppg

    shg = int(cols[12])
    shp = int(cols[13])
    sha = shp - shg

    gwg = int(cols[14])
    ot = int(cols[15])
    shots = int(cols[16])
    shot_pct = float(cols[17])

    tt = time.strptime(cols[18], "%M:%S")
    toi_gp = tt.tm_min * 60 + tt.tm_sec

    shift_gp = float(cols[19])
    fo_pct = float(cols[20])

    player = {
        'name': name,
        'team': team,
        'pos': pos,
        'gp': gp,
        'goals': goals,
        'assists': assists,
        'points': points,
        'plus_minus': plus_minus,
        'pims': pims,
        'ppg': ppg,
        'ppa': ppa,
        'ppp': ppp,
        'shg': shg,
        'sha': sha,
        'shp': shp,
        'gwg': gwg,
        'ot': ot,
        'shots': shots,
        'shot_pct': shot_pct,
        'toi_gp': toi_gp,
        'shift_gp': shift_gp,
        'fo_pct': fo_pct
    }
    return player


# Setup Urls
root_url = 'http://www.nhl.com'
stats_players_url = '/ice/playerstats.htm'

# Get the html
response = requests.get(root_url + stats_players_url)

# Get the response as a soup
soup = bs4.BeautifulSoup(response.text)

# Get the players stats table
stats_players_table = soup.find('table', {'class': ['data', 'stats']})
#print(stats_players_table)

# Get the body of the player stats table
stats_players_table_body = stats_players_table.find('tbody')

stats_players_rows = stats_players_table_body.find_all('tr')
players = []
for row in stats_players_rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]

    # Parse player stats
    player = parse_player_cols(cols)
    players.append(player)

    # data.append([ele for ele in cols if ele])  # Get rid of empty values

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(players)
