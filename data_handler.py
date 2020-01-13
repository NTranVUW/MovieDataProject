from boxofficemojo_handler import BoxOfficeMojo
from imdb_handler import IMDB
from metacrtic_handler import Metacritic
from rotten_tomatoes_handler import RottenTomatoes


class DataContainer:
    def __init__(self, wikipedia_link):
        self.imdb = None
        self.metacritic = None
        self.rotten_tomatoes = None
        self.boxofficemojo = None
        self.get_wikipedia_external_links(wikipedia_link)

    # <a rel="nofollow" class="external text" href="https://www.sitename.com/foo/"><i>Name Of The Movie</i></a>
    def get_wikipedia_external_links(self, wikipedia_link):
        from movie_lister import open_connection
        connection = open_connection(wikipedia_link)
        for item in connection.find_all('a', class_="external text"):
            self.parse_url(item['href'], wikipedia_link)

    def parse_url(self, url, wikipedia_link):
        # URLs are in the format: https://www.sitename.com/foo/
        # Splitting by . gives us: https://www . sitename . com/foo/
        # Allowing an easy way to retrieve the website name
        url_split = url.split('.')
        if len(url_split) > 1:
            url_name = url_split[1]
            # Determine which website the url belongs to
            if self.is_imdb(url, url_name, url_split) or self.is_metacritic(url, url_name, url_split) \
                    or self.is_rotten_tomatoes(url, url_name, url_split):
                return
        # An error has occurred here: The url should have been split, most likely a mistake on wikipedia
        else:
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
                # BoxOfficeMojo uses the IMDB ids for indexing: We can easily find the bom link from the imdb link
                # IMDB links are in the format: https://www.imdb.com/title/ttXXXXXXX/
                # Splitting by / gives us: https: / / www.imdb.com / title / ttXXXXXXX /
                # Thus giving us the bom link by concatenating 'ttXXXXXXX' to the end of
                # 'https://www.boxofficemojo.com/title/'
                boxofficemojo_link = ''.join(['https://www.boxofficemojo.com/title/', site.split('/')[4], '/'])
                self.boxofficemojo = BoxOfficeMojo(boxofficemojo_link)
                return True
            else:
                return False

    def is_metacritic(self, site, site_name, site_split):
        if site_name == "metacritic":
            # The /movie/ prefix indicates that this is a link to a movie: We're only interested in movies
            if site_split[2].startswith("com/movie/"):
                self.metacritic = Metacritic(site)
                return True
            else:
                return False

    def is_rotten_tomatoes(self, site, site_name, site_split):
        if site_name == "rottentomatoes":
            # The /m/ prefix indicates that this is a link to a movie: We're only interested in movies
            if site_split[2].startswith("com/m/"):
                self.rotten_tomatoes = RottenTomatoes(site)
                return True
            else:
                return False

    def predict_missing_values(self, title):
        if self.metacritic is None:
            self.metacritic = Metacritic.predict_link(title)
        return self

    def find_incorrect_urls(self, title):
        if not Metacritic.check_link(self.metacritic.link):
            print(title)
            self.metacritic.link = None














