import os

import boxofficemojo_handler
import imdb_handler
import metacritic_handler
import rotten_tomatoes_handler
import tmdb_handler
import utilities
from boxofficemojo_handler import BoxOfficeMojo
from imdb_handler import IMDB
from metacritic_handler import Metacritic
from rotten_tomatoes_handler import RottenTomatoes
from utilities import Printer


class DataContainer:
    def __init__(self, year, wikipedia_link=None, film=None):
        self.film = film
        self.year = year
        self.imdb = None
        self.metacritic = None
        self.rotten_tomatoes = None
        self.boxofficemojo = None
        self.tmdb = None
        if wikipedia_link is not None:
            self.get_wikipedia_external_links(wikipedia_link)
        if film is not None:
            self.parse_data(film)

    def parse_data(self, film):
        self.imdb = imdb_handler.IMDB.parse(film)
        self.metacritic = metacritic_handler.Metacritic.parse(film)
        self.rotten_tomatoes = rotten_tomatoes_handler.RottenTomatoes.parse(film)
        self.boxofficemojo = boxofficemojo_handler.BoxOfficeMojo.parse(film)
        if self.imdb is not None:
            # if film["TMDB"] is not None:
                # self.tmdb = tmdb_handler.TMDB.parse(self.imdb.id, film=film)
            # else:
                self.tmdb = tmdb_handler.TMDB.parse(self.imdb.id)

    # Used to find a mismatch of release year and the year displayed on the webpages
    def print_wrong_years(self):
        with open(''.join(['resources//', str(self.year), '_wrong_years.txt']), 'a') as txt_file:
            if self.imdb is not None:
                imdb_year = self.imdb.check_year(self.year)
                if imdb_year is not None:
                    txt_file.write(''.join([self.film["Name"], ": IMDB — ", imdb_year, " != ", self.year, "\n"]))

            if self.metacritic is not None:
                metacritic_year = self.metacritic.check_year(self.year)
                if metacritic_year is not None:
                    txt_file.write(''.join([self.film["Name"], ": Metacritic — ", metacritic_year, " != ",
                                            self.year, "\n"]))
            if self.rotten_tomatoes is not None:
                rotten_tomatoes_year = self.rotten_tomatoes.check_year(self.year)
                if rotten_tomatoes_year is not None:
                    txt_file.write(''.join([self.film["Name"], ": Rotten Tomatoes — ", rotten_tomatoes_year, " != ",
                                            self.year, "\n"]))

    # <a rel="nofollow" class="external text" href="https://www.sitename.com/foo/"><i>Name Of The Movie</i></a>
    def get_wikipedia_external_links(self, wikipedia_link):
        from utilities import open_connection
        connection = open_connection(wikipedia_link)
        for item in connection.find_all('a', class_="external text"):
            self.parse_url(item['href'], wikipedia_link)

    def parse_url(self, url, wikipedia_link):
        # URLs are in the format: https://www.sitename.com/foo/
        # Splitting by . gives us: https://www . sitename . com/foo/
        # Allowing an easy way to retrieve the website name
        url_split = url.split('.')
        if len(url_split) > 2:
            if url_split[0] is not 'http://www':
                url = ''.join(['http://www.', url_split[1], ".", url_split[2]])
                url_split = url.split('.')
            url_name = url_split[1]
            # Determine which website the url belongs to
            if self.is_imdb(url, url_name, url_split) or self.is_metacritic(url, url_name, url_split) \
                    or self.is_rotten_tomatoes(url, url_name, url_split):
                return
        # An error has occurred here: The url should have been split, most likely a mistake on wikipedia
        elif len(url_split) < 2:
            ss = ""
            for s in url_split:
                ss = ss + s
            # Debugging code: Print the broken url
            print("site_split: %s, site: %s, Movie: %s" % (ss, url, wikipedia_link))

    def is_imdb(self, site, site_name, site_split):
        if site_name == "imdb":
            # The /title/ prefix indicates that this isn't a link to an article
            if site_split[2].startswith("com/title/"):
                self.imdb = IMDB(site)
                Printer.print_minus(''.join(["FOUND IMDB: ", site]))
                # BoxOfficeMojo uses the IMDB ids for indexing: We can easily find the bom link from the imdb link
                # IMDB links are in the format: https://www.imdb.com/title/ttXXXXXXX/
                # Splitting by / gives us: https: / / www.imdb.com / title / ttXXXXXXX /
                # Thus giving us the bom link by concatenating 'ttXXXXXXX' to the end of
                # 'https://www.boxofficemojo.com/title/'
                boxofficemojo_link = ''.join(['https://www.boxofficemojo.com/title/', site.split('/')[4], '/'])
                self.boxofficemojo = BoxOfficeMojo(boxofficemojo_link)
                Printer.print_minus(''.join(["FOUND BOXOFFICEMOJO: ", boxofficemojo_link]))
                return True
            else:
                return False

    def is_metacritic(self, site, site_name, site_split):
        if site_name == "metacritic":
            # The /movie/ prefix indicates that this is a link to a movie: We're only interested in movies
            if site_split[2].startswith("com/movie/"):
                self.metacritic = Metacritic(site)
                Printer.print_minus(''.join(["FOUND METACRITIC: ", site]))
                return True
            else:
                return False

    def is_rotten_tomatoes(self, site, site_name, site_split):
        if site_name == "rottentomatoes":
            # The /m/ prefix indicates that this is a link to a movie: We're only interested in movies
            if site_split[2].startswith("com/m/"):
                self.rotten_tomatoes = RottenTomatoes(site)
                Printer.print_minus(''.join(["FOUND ROTTEN TOMATOES: ", site]))
                return True
            else:
                return False

    def predict_missing_values(self, title):
        if self.imdb is None:
            Printer.print_minus(''.join(["MISSING IMDB: ", title, " - ", self.year]))
            self.log_missing_link(''.join([title, ": IMDB"]))
            self.log_missing_link(''.join([title, ": Boxofficemojo"]))
        if self.metacritic is None:
            self.metacritic = Metacritic(Metacritic.predict_link(title))
            self.log_predicted_link(''.join([title, ": ", self.metacritic.link]))
        if self.rotten_tomatoes is None:
            self.rotten_tomatoes = RottenTomatoes(RottenTomatoes.predict_link(title, self.year))
            self.log_predicted_link(''.join([title, ": ", self.rotten_tomatoes.link]))
        return self

    def find_incorrect_urls(self, title):
        if self.imdb is not None:
            if not utilities.check_link(self.imdb.link):
                Printer.print_minus(''.join(["INCORRECT IMDB: ", title, " - ", self.year]))
                self.log_missing_link(''.join([title, ": IMDB"]))
                self.imdb = None
        if self.metacritic is not None:
            if not utilities.check_link(self.metacritic.link):
                Printer.print_minus(''.join(["INCORRECT METACRITIC: ", title, " - ", self.year]))
                self.log_missing_link(''.join([title, ": Metacritic"]))
                self.metacritic = None
        if self.rotten_tomatoes is not None:
            if not utilities.check_link(self.rotten_tomatoes.link):
                Printer.print_minus(''.join(["INCORRECT ROTTEN TOMATOES: ", title, " - ", self.year]))
                self.log_missing_link(''.join([title, ": Rotten Tomatoes"]))
                self.rotten_tomatoes = None
        if self.boxofficemojo is not None:
            if not utilities.check_link(self.boxofficemojo.link):
                Printer.print_minus(''.join(["INCORRECT BOXOFFICEMOJO: ", title, " - ", self.year]))
                self.log_missing_link(''.join([title, ": Boxofficemojo"]))
                self.boxofficemojo = None

    def log_missing_link(self, link):
        with open(''.join(['resources//', str(self.year), '_missing_links.txt']), 'a') as txt_file:
            txt_file.write(''.join([link, "\n"]))

    def log_predicted_link(self, link):
        with open(''.join(['resources//', str(self.year), '_predicted_links.txt']), 'a', encoding="utf-8") as txt_file:
            txt_file.write(''.join([link, "\n"]))
