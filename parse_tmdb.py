import requests
import json
import time
import movie

url = "https://api.themoviedb.org/3"
discover = "/discover/movie"
api_key = "?api_key=6df9d07a07bbfae421d8dd576e24170d"
sort = "&sort_by="
page = "&page="
prime_year = "&primary_release_year="
vote_count = "&vote_count.gte="


def parse(year, vote):
    movies = {}
    get_url = url + discover + api_key
    payload = "{}"
    response = requests.request("GET", get_url + sort + "vote_count.desc" + page + str(1) + prime_year + str(year)
                                + vote_count + str(vote), data=payload)
    print(get_url + sort + "vote_count.desc" + page + str(1) + prime_year + str(year) + vote_count + str(vote))
    print(response.content)
    time.sleep(0.25)
    file = response.json()
    total_pages = file["total_pages"]
    for i in range(total_pages):
        response = requests.request("GET", get_url + sort + "vote_count.desc" + page + str(i + 1) + prime_year
                                    + str(year) + vote_count + str(vote), data=payload)
        file = response.json()
        parse_json(file, movies)
    return movies
    # with open(str(year) + '_' + str(i) + '.json', 'w', encoding='utf-8') as f:
    # json.dump(file, f, ensure_ascii=False, indent=4)


def parse_json(file, movies):
    results = file["results"]
    for r in results:
        mov = movie.Movie(r["title"])
        mov.set_tmdb_id(r["id"])\
            .set_popularity(r["popularity"])\
            .set_vote_count(r["vote_count"])\
            .set_original_language(r["original_language"])\
            .set_original_title(r["original_title"])\
            .set_genre_ids(r["genre_ids"])\
            .set_vote_average(r["vote_average"])\
            .set_overview(r["overview"])\
            .set_release_date(r["release_date"])
        movies[r["title"]] = mov

    time.sleep(0.25)
