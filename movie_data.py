import urllib
from urllib.request import Request, urlopen

import urllib3
from bs4 import BeautifulSoup
import requests

import data_handler
import wikipedia_handler


class MovieCollection:

    def __init__(self):
        self.year = None
        self.films = None

    def set_year(self, year):
        self.year = year
        return self

    def get_films(self):
        self.films = wikipedia_handler.parse(self.year)


class Movie:
    def __init__(self, title):
        self.title = title
        self.wikipedia_link = None
        self.movie_data = None

    def set_wikipedia_link(self, link):
        self.wikipedia_link = link

    def set_movie_data(self):
        self.movie_data = data_handler.DataContainer(self.wikipedia_link)

    def check_metacritic_link(self):
        req = Request(self.metacritic_link, headers={'User-Agent': 'Mozilla/5.0'})
        html_page = ''
        try:
            html_page = urlopen(req).read()
        except urllib.error.HTTPError as e:
            if e.getcode() == 404:
                print(self.title)
                self.metacritic_link = None
        if len(str(html_page)) > 1:
            soup = BeautifulSoup(html_page, "html.parser")
            # print(soup.find('title'))
