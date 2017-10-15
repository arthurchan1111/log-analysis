#!/usr/bin/env python2.7
import psycopg2


def connect():
    try:
        db = psycopg2.connect("dbname=news")
        cursor = db.cursor()
        return db, cursor
    except:
        print "Unable to connect to database"
        sys.exit(1)


filename = "output.txt"

query_1_answer = """SELECT articles.title, article_view.views
                FROM articles, article_view
                WHERE article_view.path::text like
                concat('%',articles.slug,'%')
                ORDER BY article_view.views DESC LIMIT 3"""

query_2_answer = """ SELECT name, SUM(views) AS views
                   FROM article_view, authors_by_title
                   WHERE article_view::text like concat('%',slug,'%')
                   GROUP BY authors_by_title.name
                   ORDER BY views DESC """

query_3_answer = """SELECT errors.error_dates AS dates,
                   ROUND(((total_errors::decimal/total_success::decimal)
                   * 100),2) AS percentage
                   FROM (SELECT time::date AS error_dates,
                   COUNT(status) AS total_errors
                   FROM log
                   WHERE status='404 NOT FOUND'
                   GROUP BY time::date) AS errors,
                   (SELECT time::date AS success_dates,
                   COUNT(status) as total_success
                   FROM log GROUP BY time::date) AS successes
                   WHERE errors.error_dates = success_dates
                   AND ((total_errors::decimal/
                   total_success::decimal) * 100) > 1 """


def getquery(query):
    db, cursor = connect()
    cursor.execute(query)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result


def print_top_articles():
    f.write("What are the most popular three articles of all time?\n\n")
    q1 = getquery(query_1_answer)
    for index in range(len(q1)):
        f.write(str(index+1)+". " +
                q1[index][0]+" - " +
                str(q1[index][1])+" views" + "\n")


def print_top_authors():
    f.write("\nWho are the most popular article authors of all time?\n\n")
    q2 = getquery(query_2_answer)
    for index in range(len(q2)):
        f.write(str(index+1) +
                ". "+q2[index][0]+" - " +
                str(q2[index][1])+" views" + "\n")


def print_top_error_days():
    f.write("\nOn which days did more than 1% of requests lead to errors?\n\n")
    q3 = getquery(query_3_answer)
    for index in range(len(q3)):
        f.write(str(index+1) + ". " +
                str(q3[index][0]) + " - " +
                str(q3[index][1]) + "%" + "\n")


if __name__ == '__main__':
    f = open(filename, 'w')
    print_top_articles()
    print_top_authors()
    print_top_error_days()
    f.close()
