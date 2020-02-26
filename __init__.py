import json
import os

import parser

import movie_parser
import scraper
from utils import Printer

years = []
data = {}


def check_file_exists():
    for y in years:
        Printer.print_equal(''.join(["CREATE YEAR: ", y]))

        file_path = ''.join(['resources//', str(y), '_data.json'])
        tsv_path = ''.join(['resources//', str(y), '_data.tsv'])

        if os.path.isfile(file_path):
            Printer.print_equal('FILE EXISTS: Parsing Data...')

            data[y] = movie_parser.parse(file_path)
        elif os.path.isfile(tsv_path):
            Printer.print_equal('TSV EXISTS: Parsing TSV...')

            data[y] = movie_parser.parse_tsv(tsv_path)
        else:
            Printer.print_equal(''.join(['FILE DOES NOT EXIST: Creating ', y, ' File...']))

            data[y] = scraper.scrape(y)
            print_to_tsv(data[y], y)


def print_to_tsv(data_for_year, y):
    data_line = 'Title\tWikipedia Link\tIMDB Link\tIMDB ID\tMismatched IMDB\tRotten Tomatoes Link\t' \
                'Mismatched Rotten Tomatoes\tMetacritic Link\tMismatched Metacritic\tBox Office Mojo Link\n'

    for n in data_for_year:
        m = data_for_year[n]
        data_line = ''.join([data_line, m.name, '\t', m.link])

        if m.imdb is not None:
            if m.imdb.link is not None:
                data_line = ''.join([data_line, '\t', m.imdb.link, '\t', m.imdb.id, '\t', str(m.imdb.mismatch)])
            else:
                data_line = ''.join([data_line, '\tNone\tNone\tNone'])
        else:
            data_line = ''.join([data_line, '\tNone\tNone\tNone'])

        if m.rotten_tomatoes is not None:
            if m.rotten_tomatoes.link is not None:
                data_line = ''.join([data_line, '\t', m.rotten_tomatoes.link, '\t', str(m.rotten_tomatoes.mismatch)])
            else:
                data_line = ''.join([data_line, '\tNone\tNone'])
        else:
            data_line = ''.join([data_line, '\tNone\tNone'])

        if m.metacritic is not None:
            if m.metacritic.link is not None:
                data_line = ''.join([data_line, '\t', m.metacritic.link, '\t', str(m.metacritic.mismatch)])
            else:
                data_line = ''.join([data_line, '\tNone\tNone'])
        else:
            data_line = ''.join([data_line, '\tNone\tNone'])

        if m.box_office_mojo is not None:
            if m.box_office_mojo.link is not None:
                data_line = ''.join([data_line, '\t', m.box_office_mojo.link, '\n'])
            else:
                data_line = ''.join([data_line, 'None\n'])
        else:
            data_line = ''.join([data_line, 'None\n'])

    with open(''.join(['resources//', str(y), '_data.tsv']), 'w', encoding="utf-8") as tsv_file:
        tsv_file.write(data_line)


def save_data(y):
    data_dict = {'films': []}
    file_path = ''.join(['resources//', str(y), '_data.json'])
    with open(file_path, 'w') as json_file:
        for film_name in data[y]:
            film = data[y][film_name]
            data_dict['films'].append({
                'Name': film.name,
                "Link": film.link,
                "IMDB": save_imdb(film),
                "Metacritic": save_metacritic(film),
                "Rotten Tomatoes": save_rotten_tomatoes(film),
                "Box Office Mojo": save_box_office_mojo(film),
            })
        json.dump(data_dict, json_file)


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
        year = ''.join(['201', str(i)])

        years.append(year)

    check_file_exists()

    Printer.print_equal('SAVING FILES')

    for year in years:
        save_data(year)

Printer.print_equal('PROGRAM END')
