import utilities
from movie_data import MovieCollection
from utilities import Printer

year_dict = {}


class Year:

    def __init__(self, year_):
        Printer.print_equal(''.join(["CREATE YEAR: ", year_]))
        self.year = year_
        self.movie_data = MovieCollection(year_)


if __name__ == '__main__':
    Printer.print_equal('PROGRAM START')
    for i, item in enumerate(range(9)):
        year = ''.join(['201', str(i)])
        year_dict[year] = Year(year)
        utilities.count = 0
    Printer.print_equal('PROGRAM END')
