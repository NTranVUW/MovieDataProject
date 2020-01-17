import urllib

from unidecode import unidecode

import utilities
from utilities import Printer


class RottenTomatoes:
    def __init__(self, link):
        self.link = link

    @staticmethod
    def parse(film):
        if film["Rotten Tomatoes"] is not None:
            rt = RottenTomatoes(film["Rotten Tomatoes"]['Link'])
            return rt

    @staticmethod
    def predict_link(title, year):
        link = ''
        title_split = title.split()
        for t in title_split:
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
        new_link = urllib.parse.urljoin('https://www.rottentomatoes.com/m/', link[:-1])
        if not utilities.check_link(new_link):
            link = ''.join([link[:-1], '_', year])
            new_link = urllib.parse.urljoin('https://www.rottentomatoes.com/m/', link)

        # print(new_link)
        Printer.print_minus(''.join(["MISSING ROTTEN TOMATOES: ", title, ", Predicted Link: ", new_link]))
        return new_link
