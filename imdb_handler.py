import requests
from bs4 import BeautifulSoup


class IMDB:
    def __init__(self, link):
        self.link = link
        self.id = link.split('/')[4]

    @staticmethod
    def parse(film):
        if film["IMDB"] is not None:
            new_imdb = IMDB(film["IMDB"]["Link"])
            new_imdb.id = film["IMDB"]['ID']
            return new_imdb
        return None

    def check_year(self, year):
        req = requests.get(self.link, headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(req, 'html.parser')
        for titleYear in soup.find_all(id="titleYear"):
            y = titleYear.find('a').getText()
            if y is not None:
                if y != year and int(y) != int(year) - 1 and int(y) != int(year) + 1:
                    return y
        return None

