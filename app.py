import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template

app = Flask(__name__)

# base_url = "https://www.tvspielfilm.de/tv-programm/sendungen/zdf,ZDF.html"
base_url = "https://www.tvspielfilm.de/tv-programm/sendungen/?time=day&channel=ZDF"

def get_when(search_term):
    url = base_url
    r = requests.get(url)
    soup = soup = BeautifulSoup(r.text, "html.parser")
    trs = soup.find_all("tr")
    titles = []
    dates = []
    for tr in trs:
        try:
            tds = tr.find_all("td")
            if len(tds) > 2:
                date = tds[1].find("strong").string
                if date:
                    dates.append(date)
                
                title = tds[2].find("strong").string
                if title:
                    titles.append(title)
        except KeyError:
            """Ignore the tag that doesn't have a class atribute"""
            pass
    program = dict(zip(titles, dates))
    if (search_term in program):
        when = program[search_term]
    else:
        when = "- - -"
    return {
        "when": when,
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
