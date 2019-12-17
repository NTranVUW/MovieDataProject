import csv

file = "resources\\imdb\\title.basics\\data.tsv"


def parse(year, movies):
    with open(file, encoding="utf8") as title_basics:
        rd = csv.reader(title_basics, delimiter="\t", quotechar='"')
        first = True
        i = 0
        for r in rd:
            if first:
                first = False
            elif str(r[5]) == str(year):
                if r[2] in movies:
                    i = i + 1
                    mov = movies[r[2]]
        print(str(i) + "/" + str(len(movies)))
