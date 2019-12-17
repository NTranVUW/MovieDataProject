from bs4 import BeautifulSoup
import requests

from movie import Movie


def parse(year, films):
    url = "https://en.wikipedia.org/wiki/" + year + "_in_film"
    req = requests.get(url).text
    soup = BeautifulSoup(req, 'html.parser')

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
                            wiki_link = a['href']
                            films[title] = Movie(title, wiki_link)

