import csv
import sqlite3

path = "db.sqlite3"

use = sqlite3.connect(path)
cur = use.cursor()
with open("category.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [(i["id"], i["name"], i["slug"]) for i in directory]
cur.executemany(
    ("INSERT INTO reviews_category (id, name, slug) " "VALUES (?, ?, ?);"),
    base,
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("comments.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [
        (i["id"], i["review_id"], i["text"], i["author"], i["pub_date"])
        for i in directory
    ]
cur.executemany(
    (
        "INSERT INTO reviews_comment (id, review_id, text, author,"
        " pub_date) VALUES (?, ?, ?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("genre.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [(i["id"], i["name"], i["slug"]) for i in directory]
cur.executemany(
    ("INSERT INTO reviews_genre (id, name, slug) " "VALUES (?, ?, ?);"), base
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("genre_title.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [(i["id"], i["title_id"], i["genre_id"]) for i in directory]
cur.executemany(
    (
        "INSERT INTO reviews_title_genre (id, title_id, genre_id) "
        "VALUES (?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("review.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [
        (
            i["id"],
            i["title_id"],
            i["text"],
            i["author"],
            i["score"],
            i["pub_date"],
        )
        for i in directory
    ]
cur.executemany(
    (
        "INSERT INTO reviews_review (id, title_id, text, author, "
        "score, pub_date, title_id) VALUES (?, ?, ?, ?, ?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()

use = sqlite3.connect(path)
cur = use.cursor()
with open("titles.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [(i["id"], i["name"], i["year"], i["category"]) for i in directory]
cur.executemany(
    (
        "INSERT INTO reviews_title (id, name, year, category) "
        "VALUES (?, ?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()


use = sqlite3.connect(path)
cur = use.cursor()
with open("users.csv", "r", encoding="utf-8") as fin:
    directory = csv.DictReader(fin)
    base = [
        (
            i["id"],
            i["username"],
            i["email"],
            i["role"],
            i["bio"],
            i["first_name"],
            i["last_name"],
        )
        for i in directory
    ]
cur.executemany(
    (
        "INSERT INTO reviews_title (id, username, email, role, bio, first_name, last_name) "
        "VALUES (?, ?, ?, ?, ?, ?, ?);"
    ),
    base,
)
use.commit()
use.close()
