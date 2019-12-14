class Movie:
    def __init__(self, title):
        self.title = title
        self.tmdb_id = None
        self.popularity = None
        self.vote_count = None
        self.original_language = None
        self.original_title = None
        self.genre_ids = None
        self.vote_average = None
        self.overview = None
        self.release_date = None

    def set_tmdb_id(self, tmdb_id):
        self.tmdb_id = tmdb_id
        return self

    def set_popularity(self, pop):
        self.popularity = pop
        return self

    def set_vote_count(self, vote):
        self.vote_count = vote
        return self

    def set_original_language(self, lang):
        self.original_language = lang
        return self

    def set_original_title(self, title):
        self.original_title = title
        return self

    def set_genre_ids(self, ids):
        self.genre_ids = ids
        return self

    def set_vote_average(self, vote):
        self.vote_average = vote
        return self

    def set_overview(self, overview):
        self.overview = overview
        return self

    def set_release_date(self, date):
        self.release_date = date
        return self

