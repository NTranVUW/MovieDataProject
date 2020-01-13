from urllib.request import Request

from envs.python36.Lib import urllib
from envs.python36.Lib.urllib.request import urlopen
from unidecode import unidecode


class Metacritic:
    def __init__(self, link):
        self.link = link

    @staticmethod
    def predict_link(title):
        link = ''
        title_split = title.split()
        for t in title_split:
            word = []
            word_as_list = list(t)
            # Only add word if alphanumeric
            for c in word_as_list:
                if c.isalnum():
                    c = unidecode.unidecode(c)
                    c = c.lower()
                    word.append(c)
            # Covert byte to string
            word_as_string = ''.join(word)
            # Metacritic URLs are in the format: https://www.metacritic.com/movie/word1-word2-word3/
            # Each word in the title separated by a dash
            # No dash at the end of URL
            link = ''.join([link, word_as_string, '-']) if len(word) > 0 else ''.join([link, word_as_string])
        new_link = urllib.parse.urljoin('http://www.metacritic.com/movie/', link[:-1])
        # print(new_link)
        return new_link

    @staticmethod
    def check_link(url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            urlopen(req).read()
        except urllib.error.HTTPError as e:
            if e.getcode() == 404:
                return False
        return True
