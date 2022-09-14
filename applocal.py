import requests
from bs4 import BeautifulSoup

base_url = "https://www.tvspielfilm.de/tv-programm/sendungen/zdf,ZDF.html"

def get_when(search_term):
#    tz = pytz.timezone('Europe/Berlin')
#    today = str(datetime.datetime.now(tz).strftime("%d.%m.%Y"))
#    url = base_url + today
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
    return {
        "when": program[search_term],
        "searchTerm": search_term,
        "url": url
    }

print(get_when("heute journal"))
