import wikipedia_parser

year_dict = {}


class Year:

    def __init__(self, year):
        self.year = year
        self.films = {}
        self.get_films()

    def get_films(self):
        wikipedia_parser.parse(self.year, self.films)
        self.films["Black Panther"].get_wiki_external_links()


def create_years():
    for i in range(9):
        year = "201" + str(i)
        year_dict[year] = Year(year)


if __name__ == '__main__':
    # create_years()
    year_dict[str(2018)] = Year(str(2018))
