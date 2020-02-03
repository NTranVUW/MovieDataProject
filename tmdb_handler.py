import time
import urllib

import requests

from utilities import Printer


class TMDB:
    absolute_url = ['https://api.themoviedb.org/3/find/', '?api_key=', '&language=en-US&external_source=imdb_id']
    api_key = '6df9d07a07bbfae421d8dd576e24170d'

    def __init__(self, tmdb_id):
        self.tmdb_id = tmdb_id
        self.video = None
        self.vote_count = None
        self.vote_average = None
        self.title = None
        self.release_date = None
        self.original_language = None
        self.original_title = None
        self.genres = None
        self.backdrop_path = None
        self.adult = None
        self.overview = None
        self.poster_path = None
        self.popularity = None
        self.belongs_to_collection = None
        self.budget = None
        self.homepage = None
        self.production_companies = None
        self.production_countries = None
        self.revenue = None
        self.runtime = None
        self.spoken_languages = None
        self.status = None
        self.tagline = None

    @staticmethod
    def parse(imdb_id, film=None):
        tmdb = None
        results = None
        if film is None:
            url = ''.join([TMDB.absolute_url[0], imdb_id, TMDB.absolute_url[1], TMDB.api_key, TMDB.absolute_url[2]])
            req = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).json()
            time.sleep(0.25)
            movie_results = req["movie_results"]
            if movie_results:
                tmdb_id = movie_results[0]["id"]
                movie_url = ''.join(['https://api.themoviedb.org/3/movie/', str(tmdb_id), '?api_key=', TMDB.api_key,
                                    '&language=en-US'])
                results = requests.get(movie_url, headers={'User-Agent': 'Mozilla/5.0'}).json()
                time.sleep(0.25)
                Printer.print_minus(''.join(['PARSING TMDB: ', movie_url]))
        else:
            results = film["TMDB"]

        if results:
            tmdb = TMDB(results["id"])
            tmdb.video = results["video"]
            tmdb.vote_count = results["vote_count"]
            tmdb.vote_average = results["vote_average"]
            tmdb.title = results["title"]
            tmdb.release_date = results["release_date"]
            tmdb.original_language = results["original_language"]
            tmdb.original_title = results["original_title"]
            tmdb.genres = results["genres"]
            tmdb.backdrop_path = results["backdrop_path"]
            tmdb.adult = results["adult"]
            tmdb.overview = results["overview"]
            tmdb.poster_path = results["poster_path"]
            tmdb.popularity = results["popularity"]
            tmdb.belongs_to_collection = results["belongs_to_collection"]
            tmdb.budget = results["budget"]
            tmdb.homepage = results["homepage"]
            tmdb.production_companies = results["production_companies"]
            tmdb.production_countries = results["production_countries"]
            tmdb.revenue = results["revenue"]
            tmdb.runtime = results["runtime"]
            tmdb.spoken_languages = results["spoken_languages"]
            tmdb.status = results["status"]
            tmdb.tagline = results["tagline"]

        return tmdb
