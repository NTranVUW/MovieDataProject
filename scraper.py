import urllib

import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

from movie import Movie, IMDB, BoxOfficeMojo, Metacritic, RottenTomatoes
import utils
from utils import Printer
from utils import open_connection


def scrape(year):
    Printer.print_equal('RETRIEVING NEW DATA')

    wiki_link = ''.join(['https://en.wikipedia.org/wiki/', year, '_in_film'])
    return scrape_wikipedia(wiki_link, year)


def scrape_wikipedia(url, year):
    Printer.print_equal('SCRAPING WIKIPEDIA')

    movies = {}
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'html.parser')

    # <table class="wikitable sortable jquery-tablesorter">
    # --- <tbody>
    # ------- <tr>
    # ----------- <td>
    # --------------- <i>
    # ------------------- <a href="/wiki/Name_Of_The_Movie" title="Name Of The Movie">Name Of The Movie</a>
    for table in soup.find_all('table', class_="wikitable sortable"):
        tbody = table.find('tbody')
        for tr in tbody.find_all('tr'):
            for td in tr.find_all('td'):
                if td is not None:
                    i = td.find('i')
                    if i is not None:
                        a = i.find('a')
                        if a is not None:
                            title = a.contents[0]
                            url = ''.join(['https://en.wikipedia.org', a['href']])
                            movies[title] = Movie(url, title, year)

                            Printer.print_minus(''.join(["RETRIEVING DATA: ", str(len(movies)), ". ", title]))

                            scrape_external_links(movies[title])
                            predict_missing_links(movies[title])

    return movies


def scrape_external_links(movie):
    connection = open_connection(movie.link)
    for item in connection.find_all('a', class_="external text"):
        # URLs are in the format: https://www.sitename.com/foo/
        # Splitting by . gives us: https://www . sitename . com/foo/
        # Allowing an easy way to retrieve the website name
        url = item['href']
        url_split = url.split('.')
        if len(url_split) > 2:
            if url_split[0] is not 'http://www':
                url = ''.join(['http://www.', url_split[1], ".", url_split[2]])
                url_split = url.split('.')
            url_name = url_split[1]
            # Determine which website the url belongs to
            parse_url(url, url_name, url_split, movie)
            # An error has occurred here: The url should have been split, most likely a mistake on wikipedia
        elif len(url_split) < 2:
            ss = ""
            for s in url_split:
                ss = ss + s
            # Debugging code: Print the broken url
            print("site_split: %s, site: %s, Movie: %s" % (ss, url, movie.link))


def parse_url(url, url_name, url_split, movie):
    if url_name == 'imdb':
        parse_imdb(url, url_split, movie)
    if url_name == 'metacritic':
        parse_metacritic(url, url_split, movie)
    if url_name == 'rottentomatoes':
        parse_rottentomatoes(url, url_split, movie)


def parse_imdb(url, url_split, movie):
    # The /title/ prefix indicates that this isn't a link to an article
    if url_split[2].startswith("com/title/"):
        movie.imdb = IMDB(url, movie.name, year=movie.year)

        Printer.print_minus(''.join(["FOUND IMDB: ", url]))

        # BoxOfficeMojo uses the IMDB ids for indexing: We can easily find the bom link from the imdb link
        # IMDB links are in the format: https://www.imdb.com/title/ttXXXXXXX/
        # Splitting by / gives us: https: / / www.imdb.com / title / ttXXXXXXX /
        # Thus giving us the bom link by concatenating 'ttXXXXXXX' to the end of
        # 'https://www.boxofficemojo.com/title/'
        box_office_mojo_link = ''.join(['https://www.boxofficemojo.com/title/', url.split('/')[4], '/'])
        movie.box_office_mojo = BoxOfficeMojo(box_office_mojo_link)

        Printer.print_minus(''.join(["FOUND BOXOFFICEMOJO: ", box_office_mojo_link]))


def parse_metacritic(url, url_split, movie):
    # The /movie/ prefix indicates that this is a link to a movie: We're only interested in movies
    if url_split[2].startswith("com/movie/"):
        movie.metacritic = Metacritic(url, movie.name, year=movie.year)

        Printer.print_minus(''.join(["FOUND METACRITIC: ", url]))


def parse_rottentomatoes(url, url_split, movie):
    # The /m/ prefix indicates that this is a link to a movie: We're only interested in movies
    if url_split[2].startswith("com/m/"):
        movie.rotten_tomatoes = RottenTomatoes(url, movie.name, year=movie.year)

        Printer.print_minus(''.join(["FOUND ROTTEN TOMATOES: ", url]))


def predict_missing_links(movie):
    if movie.imdb is None:
        Printer.print_minus(''.join(["MISSING IMDB: ", movie.name, " - ", movie.year]))

    if movie.metacritic is None:
        movie.metacritic = Metacritic(predict_metacritic(movie), movie.name, year=movie.year)

    if movie.rotten_tomatoes is None:
        movie.rotten_tomatoes = RottenTomatoes(predict_rotten_tomatoes(movie), movie.name, year=movie.year)


def predict_metacritic(movie):
    link = ''
    name_split = movie.name.split()
    for t in name_split:
        word = []
        word_as_list = list(t)
        # Only add word if alphanumeric
        for c in word_as_list:
            if c.isalnum():
                c = unidecode(c)
                c = c.lower()
                word.append(c)
        # Covert byte to string
        word_as_string = ''.join(word)
        # Metacritic URLs are in the format: https://www.metacritic.com/movie/word1-word2-word3/
        # Each word in the title separated by a dash
        # No dash at the end of URL
        link = ''.join([link, word_as_string, '-']) if len(word) > 0 else ''.join([link, word_as_string])
    new_link = urllib.parse.urljoin('http://www.metacritic.com/movie/', link[:-1])

    Printer.print_minus(''.join(["MISSING METACRITIC: ", movie.name, ", Predicted Link: ", new_link]))

    return new_link


def predict_rotten_tomatoes(movie):
    link = ''
    name_split = movie.name.split()
    for t in name_split:
        word = []
        word_as_list = list(t)
        # Only add word if alphanumeric
        for c in word_as_list:
            if c.isalnum():
                c = unidecode(c)
                c = c.lower()
                word.append(c)
        # Covert byte to string
        word_as_string = ''.join(word)
        # Rotten Tomatoes URLs are in the format: https://www.rottentomatoes.com/m/word1_word2_word3
        # Each word in the title separated by an underscore
        # No underscore at the end of URL
        link = ''.join([link, word_as_string, '_']) if len(word) > 0 else ''.join([link, word_as_string])
    new_link = urllib.parse.urljoin('https://www.rottentomatoes.com/m/', link[:-1])
    if not utils.check_link(new_link):
        link = ''.join([link[:-1], '_', movie.year])
        new_link = urllib.parse.urljoin('https://www.rottentomatoes.com/m/', link)

    Printer.print_minus(''.join(["MISSING ROTTEN TOMATOES: ", movie.name, ", Predicted Link: ", new_link]))

    return new_link
