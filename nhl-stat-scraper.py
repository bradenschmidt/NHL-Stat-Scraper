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
stats_players_table = soup.select('div.contentBlock table.data.stats')

print(stats_players_table)
