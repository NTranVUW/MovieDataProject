import requests
from bs4 import BeautifulSoup

from movie_data import MovieCollection

year_dict = {}


def open_connection(url):
    req = requests.get(url).text
    return BeautifulSoup(req, 'html.parser')


class Year:

    def __init__(self, year):
        self.year = year
        self.movie_data = MovieCollection().set_year(year)


if __name__ == '__main__':
    for i in range(9):
        year = "201" + str(i)
        year_dict[year] = Year(year)
