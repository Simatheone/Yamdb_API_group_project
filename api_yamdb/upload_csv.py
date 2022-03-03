import csv
import sqlite3

path = "db.sqlite3"

use = sqlite3.connect(path)
cur = use.cursor()
with open("static/data/category.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [(i["id"], i["name"], i["slug"]) for i in directory]
cur.executemany(
    ("INSERT INTO category (id, name, slug) " "VALUES (?, ?, ?);"),
    base,
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("static/data/comments.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [
        (i["id"], i["review_id"], i["text"], i["author_id"], i["pub_date"])
        for i in directory
    ]
cur.executemany(
    (
        "INSERT INTO comments (id, review_id, text, author_id,"
        "pub_date) VALUES (?, ?, ?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("static/data/genre.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [(i["id"], i["name"], i["slug"]) for i in directory]
cur.executemany(
    ("INSERT INTO genre (id, name, slug) " "VALUES (?, ?, ?);"), base
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("static/data/genre_title.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [(i["id"], i["genre_id"], i["title_id"]) for i in directory]
cur.executemany(
    (
        "INSERT INTO reviews_title_genre (id, genre_id, title_id)"
        "VALUES (?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("static/data/review.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [
        (
            i["id"],
            i["text"],
            i["score"],
            i["pub_date"],
            i["author"],
            i["title"],
        )
        for i in directory
    ]
cur.executemany(
    (
        "INSERT INTO reviews (id, text, score, pub_date, "
        "author_id, title_id) VALUES (?, ?, ?, ?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("static/data/titles.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [(i["id"], i["name"], i["year"], i["category"]) for i in directory]
cur.executemany(
    (
        "INSERT INTO title (id, name, year, category_id)"
        "VALUES (?, ?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()


use = sqlite3.connect(path)
cur = use.cursor()
with open("static/data/users.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [
        (
            i["id"],
            i["username"],
            i["email"],
            i["role"],
        )
        for i in directory
    ]
cur.executemany(
    (
        "INSERT INTO customuser (id, username, email, role)"
        "VALUES (?, ?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()
