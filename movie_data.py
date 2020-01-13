import json

import data_handler
import os


class MovieCollection:

    def __init__(self, year):
        self.year = year
        self.films = None
        self.file = ''.join(['resources//', str(self.year), '_data.json'])
        if os.path.isfile(self.file):
            self.parse_existing_data()
        else:
            self.get_new_data()

    # TO-DO
    def parse_existing_data(self):
        with open(self.file) as json_file:
            data = json.load(json_file)

    def get_new_data(self):
        import wikipedia_handler
        self.films = wikipedia_handler.parse(self.year)
        self.create_data_containers()

    def create_data_containers(self):
        for title, film in self.films.items():
            film.movie_data = data_handler.DataContainer(film.wikipedia_link)
            film.movie_data.predict_missing_values(title).find_incorrect_urls(title)


class Movie:
    def __init__(self, title, wikipedia_link):
        self.title = title
        self.wikipedia_link = wikipedia_link
        self.movie_data = None
