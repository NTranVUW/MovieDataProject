import requests
from bs4 import BeautifulSoup


# Scrapes the wikipedia pages by year: Retrieving the names and wikipedia links of all films
from movie_data import Movie
from utilities import Printer


def parse(year):
    Printer.print_equal('SCRAPING WIKIPEDIA')
    films = {}
    url = ''.join(['https://en.wikipedia.org/wiki/', year, '_in_film'])
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'html.parser')

    # <table class="wikitable sortable jquery-tablesorter">
    # --- <tbody>
    # ------- <tr>
    # ----------- <td>
    # --------------- <i>
    # ------------------- <a href="/wiki/Name_Of_The_Movie" title="Name Of The Movie">Name Of The Movie</a>
    for table in soup.find_all('table', class_="wikitable sortable"):
        tbody = table.find('tbody')
        for tr in tbody.find_all('tr'):
            for td in tr.find_all('td'):
                if td is not None:
                    i = td.find('i')
                    if i is not None:
                        a = i.find('a')
                        if a is not None:
                            title = a.contents[0]
                            url = ''.join(['https://en.wikipedia.org', a['href']])
                            films[title] = Movie(title, url)
    return films
