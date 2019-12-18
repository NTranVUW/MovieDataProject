from bs4 import BeautifulSoup
import requests


class Movie:
    def __init__(self, title, wiki_link):
        self.title = title
        self.wiki_link = "https://en.wikipedia.org" + wiki_link
        self.imdb_link = None
        self.metacritic_link = None
        self.rottentomatoes_link = None
        self.boxofficemojo_link = None

    def get_wiki_external_links(self):
        url = self.wiki_link
        req = requests.get(url).text
        soup = BeautifulSoup(req, 'html.parser')
        for item in soup.find_all('a', class_="external text"):
            site = item['href']
            site_split = site.split('.')
            if len(site_split) > 1:
                site_name = site_split[1]
            if site_name == "imdb":
                if site_split[2].startswith("com/title/"):
                    self.imdb_link = site
            elif site_name == "metacritic":
                if site_split[2].startswith("com/movie/"):
                    self.metacritic_link = site
            elif site_name == "rottentomatoes":
                if site_split[2].startswith("com/m/"):
                    self.rottentomatoes_link = site
            elif site_name == "boxofficemojo":
                if site_split[2].startswith("com/movies/"):
                    self.boxofficemojo_link = site
