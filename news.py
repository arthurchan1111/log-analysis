import psycopg2


def connect():
    return psycopg2.connect("dbname=news")


def query1():
    db = connect()
    cursor = db.cursor()
    query_1_answer = """SELECT articles.title, article_view.views
                    FROM articles, article_view
                    WHERE article_view.path::text like
                    concat('%',articles.slug,'%')
                    ORDER BY article_view.views DESC LIMIT 3"""

    cursor.execute(query_1_answer)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result


def query2():
    db = connect()
    cursor = db.cursor()
    query_2_answer = """ SELECT name, SUM(views) AS views
                   FROM article_view, authors_by_title
                   WHERE article_view::text like concat('%',slug,'%')
                   GROUP BY authors_by_title.name
                   ORDER BY views DESC """
    cursor.execute(query_2_answer)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result


def query3():
    db = connect()
    cursor = db.cursor()
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
    cursor.execute(query_3_answer)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result

q1 = query1()
q2 = query2()
q3 = query3()

filename = "output.txt"

f = open(filename, 'w')
f.write("What are the most popular three articles of all time?\n\n")

for index in range(len(q1)):
    f.write(str(index+1)+". " +
            q1[index][0]+" - " +
            str(q1[index][1])+" views" + "\n")

f.write("\nWho are the most popular article authors of all time?\n\n")

for index in range(len(q2)):
    f.write(str(index+1) +
            ". "+q2[index][0]+" - " +
            str(q2[index][1])+" views" + "\n")

f.write("\nOn which days did more than 1% of requests lead to errors?\n\n")

for index in range(len(q3)):
    f.write(str(index+1) + ". " +
            str(q3[index][0]) + " - " +
            str(q3[index][1]) + "%" + "\n")

f.close()
