
\c news;

CREATE VIEW article_view AS
SELECT path, COUNT(status) AS views
FROM log
WHERE log.status = '200 OK' AND log.path::text LIKE '/article%'
GROUP BY path;

CREATE VIEW authors_by_title AS
SELECT articles.title, authors.name, articles.slug
FROM articles, authors
WHERE articles.author = authors.id;
