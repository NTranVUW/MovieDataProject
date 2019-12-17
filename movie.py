from bs4 import BeautifulSoup
import requests


class Movie:
    def __init__(self, title, wiki_link):
        self.title = title
        self.wiki_link = wiki_link
        self.imdb_link = None
        self.metacritic_link = None
        self.rottentomatoes_link = None
        self.boxofficemofo_link = None

    def get_wiki_external_links(self):
        url = "https://en.wikipedia.org" + self.wiki_link
        req = requests.get(url).text
        soup = BeautifulSoup(req, 'html.parser')
        for item in soup.find_all('a', class_="external text"):
            site = item['href']
            site_name = site.split('.')[1]
            if site_name == "imdb":
                self.imdb_link = site
            elif site_name == "metacritic":
                self.metacritic_link = site
                print(site)
            elif site_name == "rottentomatoes":
                self.rottentomatoes_link = site
            elif site_name == "boxofficemojo":
                self.boxofficemofo_link = site
