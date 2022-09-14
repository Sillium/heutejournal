import pytz
import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template

app = Flask(__name__)

base_url = "https://www.tvspielfilm.de/tv-programm/sendungen/zdf,ZDF.html"

def get_when(search_term):
#    tz = pytz.timezone('Europe/Berlin')
#    today = str(datetime.datetime.now(tz).strftime("%d.%m.%Y"))
#    url = base_url + today
    url = base_url
    r = requests.get(url)
    soup = soup = BeautifulSoup(r.text, "html.parser")
    trs = soup.findAll("tr")
    titles = []
    dates = []
    for tr in trs:
#        for string in tr.stripped_strings:
#            print(repr(string))
        try:
            print(f"content[1]:")
            for string in tr.contents[1].stripped_strings:
                print(repr(string))
            d = str(tr.contents[1]).strip()
            if d:
                dates.append(d)

            print(f"content[2]:")
            for string in tr.contents[2].stripped_strings:
                print(repr(string))
            t = str(tr.contents[2]).strip()
            if t:
                titles.append(t)            
        except KeyError:
            """Ignore the tag that doesn't have a class atribute"""
            pass
    program = dict(zip(titles, dates))
    print(program)
    return {
        "when": program[search_term],
        "searchTerm": search_term,
        "url": url
    }

@app.route("/json")
def json():
    return get_when("heute journal")

@app.route("/plain")
def plain_text():
    return get_when("heute journal")["when"]

@app.route("/")
def index():
    answer = "Das heute journal kommt heute um " + get_when("heute journal")["when"] + " im ZDF."
    return render_template("index.html", when=answer, url=get_when("heute journal")["url"])

@app.after_request
def add_security_headers(response):
    response.headers['Cache-Control'] = 'max-age=300'
    return response
