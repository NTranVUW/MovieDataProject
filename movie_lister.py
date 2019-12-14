import parse_tmdb

years = []


class Year:

    def __init__(self, year, vote):
        self.year = year
        self.movies = None
        self.vote = vote
        self.parse(self)

    @staticmethod
    def parse(self):
        self.movies = parse_tmdb.parse(self.year, self.vote)


if __name__ == '__main__':
    years.append(Year(2019, 40))
    years.append(Year(2018, 125))
    years.append(Year(2017, 152))
    years.append(Year(2016, 154))
    years.append(Year(2015, 138))
    years.append(Year(2014, 152))
    years.append(Year(2013, 127))
    years.append(Year(2012, 92))
    years.append(Year(2011, 99))
    years.append(Year(2010, 91))




