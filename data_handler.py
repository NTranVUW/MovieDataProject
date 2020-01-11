import movie_lister2


class DataContainer:
    def __init__(self, wikipedia_link):
        self.wikipedia_link = wikipedia_link
        self.imdb = None
        self.metacritic = None
        self.rotten_tomatoes = None
        self.boxofficemojo = None
        self.get_wikipedia_external_links()

    # <a rel="nofollow" class="external text" href="https://www.sitename.com/foo/"><i>Name Of The Movie</i></a>
    def get_wikipedia_external_links(self):
        connection = movie_lister2.open_connection(self.wikipedia_link)
        for item in connection.find_all('a', class_="external text"):
            site = item['href']
            self.parse_url(site)

    def parse_url(self, site):
        # URLs are in the format: https://www.sitename.com/foo/
        # Splitting by . gives us: https://www . sitename . com/foo/
        # Allowing an easy way to retrieve the website name
        site_split = site.split('.')
        site_name = ""
        if len(site_split) > 1:
            site_name = site_split[1]
        # An error has occurred here: The url should have been split, most likely a mistake on wikipedia
        else:
            ss = ""
            for s in site_split:
                ss = ss + s
            # Debugging code: Print the broken url
            print("site_split: " + ss + ", site: " + site + ", Movie: " + self.wikipedia_link)

            if self.is_imdb(site, site_name, site_split) or self.is_metacritic(site, site_name, site_split) \
                    or self.is_rotten_tomatoes(site, site_name, site_split):
                return

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
                boxofficemojo_link = 'https://www.boxofficemojo.com/title/' + site.split('/')[4] + '/'
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

    # TO_DO:
    def predict_missing_values(self):
        if self.imdb is None:


class Data:
    def __init__(self, link):
        self.link = link


class IMDB(Data):
    def __init__(self, link):
        super().__init__(link)

    def predict_link(self):


    def check_link(self, link):
        connection = movie_lister2.open_connection(link)
        return

class Metacritic(Data):
    def __init__(self, link):
        super().__init__(link)

    def check_link(self, link):
        connection = movie_lister2.open_connection(link)
        return


class RottenTomatoes(Data):
    def __init__(self, link):
        super().__init__(link)

    def check_link(self, link):
        connection = movie_lister2.open_connection(link)
        return


class BoxOfficeMojo(Data):
    def __init__(self, link):
        super().__init__(link)

    def check_link(self, link):
        connection = movie_lister2.open_connection(link)
        return
