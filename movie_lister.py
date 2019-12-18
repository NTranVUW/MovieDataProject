import wikipedia_parser
import time
import json

from movie import Movie

year_dict = {}


class Year:

    def __init__(self, year):
        self.year = year
        self.films = {}
        self.parse_film_data()
        # self.get_films()
        # self.print_to_json()

    def get_films(self):
        wikipedia_parser.parse(self.year, self.films)
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
                film_obj.metacritic_link = film["metacritic"]
                film_obj.rottentomatoes_link = film["rottentomatoes"]
                film_obj.boxofficemojo_link = film["boxofficemojo"]
                self.films[film_title] = film_obj


def create_years():
    for i in range(9):
        year = "201" + str(i)
        year_dict[year] = Year(year)


if __name__ == '__main__':
    create_years()
