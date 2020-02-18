import json
import os

import parser
import scraper
from utils import Printer

years = []
data = {{}}


def check_file_exists():
    for y in years:
        file_path = ''.join(['resources//', str(y), '_data.json'])
        if os.path.isfile(file_path):
            Printer.print_equal('FILE EXISTS: Parsing Data...')

            data[y] = parser.parse(file_path)
        else:
            Printer.print_equal('FILE DOES NOT EXIST: Creating File...')

            data[y] = scraper.scrape(y)
            print_to_tsv(data[y], y)


def print_to_tsv(data_for_year, y):
    data_line = 'Title\tWikipedia Link\tIMDB Link\tIMDB ID\tRotten Tomatoes Link\tMetacritic Link\t' \
                'Box Office Mojo Link\tMismatched IMDB\tMismatched Rotten Tomatoes\tMismatched Metacritic\n'
    for m in data_for_year:
        data_line = ''.join([data_line, m.title, '\t', m.link, '\t', m.imdb.link, '\t', m.imdb.id, '\t',
                             m.rotten_tomatoes.link, '\t', m.metacritic.link, '\t', m.box_office_mojo.link, '\t',
                             m.imdb.mismatch, '\t', m.rotten_tomatoes.mismatch, '\t', m.metacritic.mismatch, '\t',
                             '\n'])

    with open(''.join(['resources//', str(y), '_data.tsv']), 'w') as tsv_file:
        tsv_file.write(data_line)


def save_data(y):
    data_dict = {'films': []}
    file_path = ''.join(['resources//', str(y), '_data.json'])
    with open(file_path, 'w') as json_file:
        for film_name in data[y]:
            film = data[y][film_name]
            data_dict['films'].append({
                'Name': film.title,
                "Link": film.wikipedia_link,
                "IMDB": save_imdb(film),
                "Metacritic": save_metacritic(film),
                "Rotten Tomatoes": save_rotten_tomatoes(film),
                "Box Office Mojo": save_box_office_mojo(film),
            })
        json.dump(data, json_file)


def save_imdb(movie):
    if movie.imdb is not None:
        return {
            'ID': movie.imdb.id,
            "Link": movie.imdb.link
        }
    return None


def save_metacritic(movie):
    if movie.metacritic is not None:
        return {
            'Link': movie.metacritic.link
        }
    return None


def save_rotten_tomatoes(movie):
    if movie.rotten_tomatoes is not None:
        return {
            'Link': movie.rotten_tomatoes.link
        }
    return None


def save_box_office_mojo(movie):
    if movie.box_office_mojo is not None:
        return {
            'Link': movie.box_office_mojo.link
        }
    return None


if __name__ == '__main__':
    Printer.print_equal('PROGRAM START')

    for i, item in enumerate(range(9)):
        year = ''.join(['201', i])

        Printer.print_equal(''.join(["CREATE YEAR: ", year]))

        years.append(year)

    check_file_exists()

    Printer.print_equal('SAVING FILES')

    for year in years:
        save_data(year)

Printer.print_equal('PROGRAM END')
