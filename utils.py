import sqlite3

from flask import jsonify, app


def connection(query, db='netflix.db'):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
    return result


def search_by_names(name, name1):
    sql = f"SELECT `cast` " \
          f"FROM netflix " \
          f"WHERE `cast` LIKE '%{name}%' AND `cast` LIKE '%{name1}%'"
    result = connection(sql)
    result = [{'cast': i[0]} for i in result]
    return result


# print(search_by_names('Jack Black', 'Dustin Hoffman'))


def search_type(film_type, year, genre):
    sql = f"SELECT `title`, `description`" \
          f"FROM netflix " \
          f"WHERE `type` LIKE '%{film_type}%' AND `release_year` LIKE '%{year}%' AND `listed_in` LIKE '%{genre}%'"
    result = connection(sql)
    result = [{'title': i[0], 'description': i[1]} for i in result]
    return result


# print(search_type('Movie', 2008, 'Action'))
