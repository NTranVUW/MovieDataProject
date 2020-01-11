import requests
from bs4 import BeautifulSoup

from movie_data import Movie


# Scrapes the wikipedia pages by year: Retrieving the names and wikipedia links of all films
def parse(year):
    films = {}
    url = "https://en.wikipedia.org/wiki/" + year + "_in_film"
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
                            movie = Movie(title)
                            movie.set_wikipedia_link('https://en.wikipedia.org' + a['href'])
                            films[title] = movie

    return films
