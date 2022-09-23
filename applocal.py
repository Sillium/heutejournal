import pytz
import datetime
from pytz import timezone
import requests
from bs4 import BeautifulSoup


def get_todays_act(day):
    tz = pytz.timezone('Europe/Berlin')
    today = str(datetime.datetime.now(tz).strftime("%d.%m.%Y"))
    year = str(datetime.datetime.now(tz).strftime("%Y"))

    url = f"https://www.e-werk-cologne.com/programm/monat/programm-{year}.html"

    r = requests.get(url)
    soup = soup = BeautifulSoup(r.text, "html.parser")
    divs = soup.find_all("div", {"class": "csc-textpic"})
    titles = []
    dates = []
    for div in divs:
        try:
            print(div)
        #     tds = tr.find_all("td")
        #     if len(tds) > 2:
        #         date = tds[1].find("strong").string
        #         if date:
        #             dates.append(date)
                
        #         title = tds[2].find("strong").string
        #         if title:
        #             titles.append(title)
        except KeyError:
            """Ignore the tag that doesn't have a class atribute"""
            pass
    program = dict(zip(titles, dates))
    return
    
    return {
        "act": program[day]
    }

get_todays_act("15.09.2022")
