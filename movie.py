import requests
from bs4 import BeautifulSoup

import utils
from utils import Printer


class Movie:
    def __init__(self, link, name, year=None):
        self.link = link
        self.name = name
        self.year = year

        self.imdb = None
        self.metacritic = None
        self.rotten_tomatoes = None
        self.box_office_mojo = None
        self.tmdb = None


class IMDB:
    def __init__(self, link, title, year=None):
        self.link = IMDB.check_url(link, title) if year is not None else self.link = link
        self.id = None
        if link is not None:
            self.id = link.split('/')[4]
        self.mismatch = self.check_year(year) if year is not None else self.mismatch = False

    @staticmethod
    def check_url(link, title):
        if not utils.check_link(link):
            Printer.print_minus(''.join(["INCORRECT IMDB: ", title]))

            return None
        return link

    def check_year(self, year):
        req = requests.get(self.link, headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(req, 'html.parser')
        for titleYear in soup.find_all(id="titleYear"):
            y = titleYear.find('a').getText()
            if y is not None:
                if y != year and int(y) != int(year) - 1 and int(y) != int(year) + 1:
                    return True
        return False


class BoxOfficeMojo:
    def __init__(self, link, title):
        self.link = BoxOfficeMojo.check_url(link, title)

    @staticmethod
    def check_url(link, title):
        if not utils.check_link(link):
            Printer.print_minus(''.join(["INCORRECT BOXOFFICEMOJO: ", title]))

            return None
        return link


class Metacritic:
    def __init__(self, link, title, year=None):
        self.link = Metacritic.check_url(link, title) if year is not None else self.link = link
        self.mismatch = self.check_year(year) if year is not None else self.mismatch = False

    @staticmethod
    def check_url(link, title):
        if not utils.check_link(link):
            Printer.print_minus(''.join(["INCORRECT METACRITIC: ", title]))

            return None
        return link

    def check_year(self, year):
        req = requests.get(self.link, headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(req, 'html.parser')
        for release_year in soup.find_all(class_="release_year lighter"):
            y = release_year.getText()
            if isinstance(y, int):
                if y != year and int(y) != int(year) - 1 and int(y) != int(year) + 1:
                    return True
        return False


class RottenTomatoes:
    def __init__(self, link, title, year=None):
        self.link = RottenTomatoes.check_url(link, title) if year is not None else self.link = link
        self.mismatch = self.check_year(year) if year is not None else self.mismatch = False

    @staticmethod
    def check_url(link, title):
        if not utils.check_link(link):
            Printer.print_minus(''.join(["INCORRECT ROTTEN TOMATOES: ", title]))

            return None
        return link

    def check_year(self, year):
        req = requests.get(self.link, headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(req, 'html.parser')
        for meta_row in soup.find_all(class_="meta-row clearfix"):
            meta_label = meta_row.find(class_="meta-label subtle")
            if meta_label.getText() == 'In Theaters: ':
                datetime = meta_row.find(class_="meta-value").find('time').attrs.get('datetime')
                y = datetime.split('-')[0]
                if y is not None:
                    if y != year and int(y) != int(year) - 1 and int(y) != int(year) + 1:
                        return True
        return False
