
class IMDB:
    def __init__(self, link):
        self.link = link
        self.id = link.split('/')[4]

    @staticmethod
    def parse(film):
        if film["IMDB"] is not None:
            new_imdb = IMDB(film["IMDB"]["Link"])
            new_imdb.id = film["IMDB"]['ID']
            return new_imdb
        return None
