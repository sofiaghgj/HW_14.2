from flask import Flask, app, jsonify
import sqlite3

app = Flask(__name__)


def connection(query, db='netflix.db'):
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
    return result


@app.route("/movie/<title>/")
def film_search(title):
    sql = f"SELECT `title`, `country`, `release_year`, `listed_in`, `description`" \
          f" FROM netflix " \
          f"WHERE `title` = '{title}'" \
          f"ORDER BY `release_year`"
    result = connection(sql)
    result = [{'title': i[0], 'country': i[1], 'release_year': i[2], 'genre': i[3], 'description': i[4]} for i in
              result]
    return jsonify(result)


@app.route("/movie/<int:year1>/to/<int:year2>/")
def year_search(year1, year2):
    sql = f"SELECT `title`, `release_year` " \
          f"FROM netflix " \
          f"WHERE `release_year` BETWEEN {year1} AND {year2}"
    result = connection(sql)
    result = [{'title': i[0], 'release_year': i[1]} for i in result]
    return jsonify(result)


@app.route("/rating/<rating>/")
def rating_search(rating):
    if rating == "children":
        sql = f"SELECT `title`, `rating`, `description`" \
              f" FROM netflix " \
              f"WHERE `rating` in ('G')"

    elif rating == "family":
        sql = f"SELECT `title`, `rating`, `description`" \
              f" FROM netflix " \
              f"WHERE `rating` in ('G', 'PG', 'PG-13')"
    elif rating == "adult":
        sql = f"SELECT `title`, `rating`, `description`" \
              f" FROM netflix " \
              f"WHERE `rating` in ('R', 'NC-17')"
    else:
        return ''
    result = connection(sql)
    result = [{'title': i[0], 'rating': i[1], 'description': i[2]} for i in result]
    return jsonify(result)


@app.route("/genre/<genre>/")
def genre_search(genre):
    sql = f"SELECT `title`, `description` " \
          f"FROM netflix " \
          f"WHERE `listed_in` LIKE  '%{genre}%'" \
          f" ORDER BY `release_year` DESC"
    result = connection(sql)
    result = [{'title': i[0], 'description': i[1]} for i in result][:10]
    return jsonify(result)


if __name__ == '__main__':
    app.run()
