from urllib import parse

from envs.python36.Lib import urllib
from envs.python36.Lib.urllib import parse

import time
import json
import unidecode

from movie_data import Movie

year_dict = {}


def get_missing_metacritic(title):
    link = ''
    title_split = title.split()
    for t in title_split:
        word = []
        word_as_list = list(t)
        for c in word_as_list:
            if c.isalnum():
                c = unidecode.unidecode(c)
                c = c.lower()
                word.append(c)
        word_as_string = ''.join(word)
        link = link + word_as_string + '-' if len(word) > 0 else link + word_as_string

    new_link = urllib.parse.urljoin('http://www.metacritic.com/movie/', link[:-1])
    print(new_link)
    return new_link


class Year:

    def __init__(self, year):
        self.year = year
        self.films = {}
        self.parse_film_data()
        # self.get_films()
        if year == '2018':
            self.remove_invalid_metacritic_links()
        self.print_to_json()

    def get_films(self):
        # wikipedia_parser.parse(self.year, self.films)
        for film in self.films:
            self.films[film].get_wiki_external_links()

    def print_to_json(self):
        data = {'films': []}
        for film_name in self.films:
            film = self.films[film_name]
            data["films"].append({
                'title': film.title,
                'wikipedia': film.wiki_link,
                'imdb': film.imdb_link,
                'metacritic': film.metacritic_link,
                'rottentomatoes': film.rottentomatoes_link,
                'boxofficemojo': film.boxofficemojo_link
            })
        with open('resources\\' + str(self.year) + '_data.json', 'w') as file:
            json.dump(data, file)

    def parse_film_data(self):
        with open('resources//' + str(self.year) + '_data.json') as json_file:
            data = json.load(json_file)
            for film in data["films"]:
                film_title = film["title"]
                film_obj = Movie(film_title, film["wikipedia"])
                film_obj.imdb_link = film["imdb"]
                film_obj.metacritic_link = film["metacritic"]  # if film["metacritic"] is not None \
                # else get_missing_metacritic(film_title)
                film_obj.rottentomatoes_link = film["rottentomatoes"]
                film_obj.boxofficemojo_link = film["boxofficemojo"]
                self.films[film_title] = film_obj

    def remove_invalid_metacritic_links(self):
        for film_name in self.films:
            film = self.films[film_name]
            film.check_metacritic_link()


def create_years():
    for i in range(9):
        year = "201" + str(i)
        year_dict[year] = Year(year)


if __name__ == '__main__':
    create_years()
