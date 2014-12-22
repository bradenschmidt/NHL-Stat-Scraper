## NHL.com Stats Scraper
## Braden Schmidt

# Imports
import requests
import bs4
import time
import pprint
import csv
import collections
import datetime


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

    player = collections.OrderedDict()

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
        'hits': 'NA',
        'bs': 'NA',
        'age': 'NA'
    }

    return collections.OrderedDict(player)


def add_hits_bs_to_skaters(cols, skaters):
# Cols is the skaters row
# skaters is the current list of skaters
# Returns the skaters list with hits and blocks added to the skaters dict
    name = cols[1]
    team = cols[2]
    hits = cols[6]
    bs = cols[7]

    for skater in skaters:
        if (skater['name'] == name) and (skater['team'] == team):
            skater['hits'] = hits
            skater['bs'] = bs

    return skaters


def add_age_to_skaters(cols, skaters):
# Cols is the skaters row
# skaters is the current list of skaters
# Returns the skaters list with hits added to the skaters dict
    name = cols[1]
    team = cols[2]
    dob = cols[4]

    dob_syear = dob[-2:]

    if int(dob_syear) > 50:
        dob_year = '19' + str(dob_syear)
    else:
        dob_year = '20' + str(dob_syear)

    age = datetime.date.today().year - int(dob_year)

    for skater in skaters:
        if (skater['name'] == name) and (skater['team'] == team):
            skater['age'] = age

    return skaters


def output_csv(filename, players):
    with open(filename, 'w') as f:
        ordered_fieldnames = collections.OrderedDict([('season', None),
                                                    ('name', None),
                                                    ('age', None),
                                                    ('team', None),
                                                    ('pos', None),
                                                    ('gp', None),
                                                    ('goals', None),
                                                    ('assists', None),
                                                    ('points', None),
                                                    ('plus_minus', None),
                                                    ('gwg', None),
                                                    ('pims', None),
                                                    ('ppg', None),
                                                    ('ppa', None),
                                                    ('ppp', None),
                                                    ('shg', None),
                                                    ('sha', None),
                                                    ('shp', None),
                                                    ('hits', None),
                                                    ('ot', None),
                                                    ('shots', None),
                                                    ('shot_pct', None),
                                                    ('toi_gp', None),
                                                    ('shift_gp', None),
                                                    ('fo_pct', None),
                                                    ('hits', None),
                                                    ('bs', None)])

        fp = csv.DictWriter(f, fieldnames=ordered_fieldnames)
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
    MAX_PAGE = 2

    skaters = []
    for page in range(1, MAX_PAGE):
        # Get the Skaters Info from Summary
        skaters_url = (ROOT_URL + summary_option
                       + season_option + season + fetchKey_skater_option
                       + page_option + str(page)
                       + sort_option + 'points')

        rows = get_rows(skaters_url)

        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            # Parse skater stats
            skater = parse_skater_cols(cols, season)
            skaters.append(skater)

        time.sleep(1)

    for page in range(1, MAX_PAGE+3):
        # Get the Skaters Info from Real Time Stats (HAS HITS)
        hits_url = (ROOT_URL + hits_option
                    + season_option + season + fetchKey_skater_option
                    + page_option + str(page)
                    + sort_option + 'gamesPlayed')

        rows = get_rows(hits_url)
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            skaters = add_hits_bs_to_skaters(cols, skaters)

        time.sleep(1)

    for page in range(1, MAX_PAGE+3):
        # Get the Skaters Info from Bios (HAS DOB)
        age_url = (ROOT_URL + age_option
                   + season_option + season + fetchKey_skater_option
                   + page_option + str(page)
                   + sort_option + 'points')

        rows = get_rows(age_url)
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            skaters = add_age_to_skaters(cols, skaters)

        time.sleep(1)

    return skaters


## Setup Urls
# Options: position, season, viewName, page
# viewName will be first so do not use &
ROOT_URL = 'http://www.nhl.com/ice/playerstats.htm?'
summary_option = 'viewName=summary'
hits_option = 'viewName=rtssPlayerStats'
age_option = 'viewName=bios'

# Dynamic Options
page_option = '&pg='
sort_option = '&sort='

# &Season2ALLGAGALL as playoffs year (20142015 = &20152ALLGAGALL)
season_option = '&fetchKey='
fetchKey_goalie_option = '2ALLGAGALL'
fetchKey_skater_option = '2ALLSASALL'

# Season options
# SEASONS = {'2015', '2014', '2013', '2012', '2011'}
SEASONS = {'2014'}

# Run stat collection for all selected Seasons
for season in SEASONS:
    skaters = get_skater_stats(season)

    # Pretty print the player list
    pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(skaters)

    output_csv('skaters' + season + '.csv', skaters)
