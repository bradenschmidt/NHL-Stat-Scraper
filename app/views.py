from app import app
import app.nhl_stat_scraper as nhl_stat_scraper
from flask import redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/nhl')
def nhl():
    l = {2014}
    #nhl_stat_scraper.main(l)

    return redirect(url_for('csv'))
