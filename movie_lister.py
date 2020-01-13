import requests
from bs4 import BeautifulSoup

from movie_data import MovieCollection


def open_connection(url):
    req = requests.get(url).text
    return BeautifulSoup(req, 'html.parser')


year_dict = {}


class Year:

    def __init__(self, year_):
        self.year = year_
        self.movie_data = MovieCollection(year_)


if __name__ == '__main__':
    for i, item in enumerate(range(9)):
        year = ''.join(['201', str(i)])
        year_dict[year] = Year(year)
