# Log Analysis


## Dependencies

[Python 2.7.14](https://www.python.org/downloads/)

[Postgresql](https://www.postgresql.org/download/)

If using vagrant you can ignore the above:

[VirtualBox](https://www.virtualbox.org/wiki/Downloads)

[Vagrant](https://www.vagrantup.com/downloads.html)

[Vagrant Config File](https://github.com/udacity/fullstack-nanodegree-vm)

## Installation

### Vagrant Users

1. In the root directory use the command:

```
vagrant up
```

2. Once finished type in:

```
vagrant ssh
```

3. Once logged in type:

```
cd /vagrant
```
### Get this repository

In your terminal type in:

```
git clone https://github.com/arthurchan1111/catalog.git

```
Or download the repository [here](https://github.com/arthurchan1111/catalog.git)

If using vagrant:

Copy the files into catalog directory of the [Vagrant Config File](https://github.com/udacity/fullstack-nanodegree-vm)

### Setup Database and views

1. Download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

2. Unpack the zip file and in terminal type in:

```
psql -d news -f newsdata.sql

```

3. To create the views used in this database type the command:

```
psql -d news -f viewnews.sql

```

... or

... Connect to the database with:

 ```
psql -d news

```

... Then copy and paste these directly into the terminal window:

```
CREATE VIEW article_view AS
SELECT path, COUNT(status) AS views
FROM log
WHERE log.status = '200 OK' AND log.path::text LIKE '/article%'
GROUP BY path;

```

```
CREATE VIEW authors_by_title AS
SELECT articles.title, authors.name, articles.slug
FROM articles, authors
WHERE articles.author = authors.id;

```

### Startup

1. Use to command below and you should see the results in **output.txt**

```
python news.py

```
