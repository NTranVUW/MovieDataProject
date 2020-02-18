import json

from movie import Movie, RottenTomatoes, Metacritic, BoxOfficeMojo
from utils import Printer


def parse(file):
    films = {}
    with open(file) as json_file:
        data = json.load(json_file)
        for film in data['films']:
            movie_title = film['Name']
            movie_wiki_link = film['Link']
            movie = Movie(movie_wiki_link, movie_title)
            films[movie_title] = movie

            Printer.print_minus(''.join(['PARSING: ', str(len(films)), ". ", movie_title]))

            if film['IMDB'] is not None:
                imdb_link = film['IMDB']['Link']
                movie.imdb = IMDB(imdb_link, movie_title)

            if film['Rotten Tomatoes'] is not None:
                rt_link = film['Rotten Tomatoes']['Link']
                movie.rotten_tomatoes = RottenTomatoes(rt_link, movie_title)

            if film['Metacritic'] is not None:
                meta_link = film['Metacritic']['Link']
                movie.metacritic = Metacritic(meta_link, movie_title)

            if film['Boxofficemojo'] is not None:
                bom_link = film['Boxofficemojo']['Link']
                movie.box_office_mojo = BoxOfficeMojo(bom_link, movie_title)

    return films
