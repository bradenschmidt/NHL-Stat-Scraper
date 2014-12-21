## NHL.com Stats Scraper
## Braden Schmidt

# Imports
import requests
import bs4

# Setup Urls
root_url = 'http://www.nhl.com'

stats_players_url = '/ice/playerstats.htm'

response = requests.get(root_url + stats_players_url)

soup = bs4.BeautifulSoup(response.text)
stats_players_table = soup.find('table', {'class': ['data', 'stats']})
# print(stats_players_table)

stats_players_table_body = stats_players_table.find('tbody')


stats_players_rows = stats_players_table_body.find_all('tr')

data = []
for row in stats_players_rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele])  # Get rid of empty values

print(data)
