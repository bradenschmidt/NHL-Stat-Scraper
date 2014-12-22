## NHL.com Stats Scraper
## Braden Schmidt

# Imports
import requests
import bs4
import time
import pprint
import csv
import collections


### Functions
def parse_skater_cols(cols, season):
## Takes a list of columns and parses to their stat

    name = cols[1]
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
        'season': season,
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
        'fo_pct': fo_pct,
        'hits': 'NA'
    }

    return collections.OrderedDict(player)


def add_hits_to_skaters(cols, skaters):
# Cols is the skaters row
# skaters is the current list of skaters
# Returns the skaters list with hits added to the skaters dict
    name = cols[1]
    team = cols[2]
    hits = cols[6]

    print ('\nHITS:\n' + name + team)

    for skater in skaters:
        if (skater['name'] == name) and (skater['team'] == team):
            skater['hits'] = hits

    return skaters


def output_csv(filename, players):
    with open(filename, 'w') as f:
        fp = csv.DictWriter(f, players[0].keys())
        fp.writeheader()
        fp.writerows(players)


def get_rows(url):
# Get table rows from given url
    response = requests.get(url)
    print(url)
    #print(response.text)

    # Get the response as a soup
    soup = bs4.BeautifulSoup(response.text)

    # Get the players stats table
    table = soup.find('table', {'class': ['data', 'stats']})
    #print(stats_players_table)

    # Get the body of the player stats table
    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    return rows


def get_skater_stats(season):
# Get the skater stats with hits for the given season
# Return the skaters
    MAX_PAGE = 15
    POSITION = 'S'

    skaters = []
    for page in range(1, MAX_PAGE+1):
        # Get the Skaters Info from Summary
        skaters_url = (ROOT_URL + players_option
                       + position_option + POSITION
                       + season_option + SEASON
                       + page_option + str(page))

        rows = get_rows(skaters_url)

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            # Parse skater stats
            skater = parse_skater_cols(cols, SEASON)
            skaters.append(skater)

        time.sleep(1)

    for page in range(1, MAX_PAGE):
        # Get the Skaters Info from Real Time Stats (HAS HITS)
        hits_url = (ROOT_URL + 'viewName=rtssPlayerStats'
                    + position_option + POSITION
                    + season_option + SEASON
                    + page_option + str(page))

        rows = get_rows(hits_url)
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            skaters = add_hits_to_skaters(cols, skaters)

        time.sleep(1)

    return skaters


# Setup Url
# Options: position, season, viewName, page
# viewName will be first so do not use &
ROOT_URL = 'http://www.nhl.com/ice/playerstats.htm?'
players_option = 'viewName=summary'
hits_option = 'viewName=rtssPlayerStats'

# Dynamic Options
position_option = '&position='
season_option = '&season='
page_option = '&pg='

# Season options
SEASONS = {'20142015', '20132014', '20122013', '20112012', '20102011'}
SEASON = '20142015'

skaters = get_skater_stats(SEASON)

# Pretty print the player list
pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(skaters)

output_csv('skaters.csv', skaters)
