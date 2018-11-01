# temporalite (In Active Development)
A Python module which aims to implement temporal databases by using python's built-in sqlite3 module.


## Status

### Create Query

Able to create tables.

```
>>> import temporalite
>>> connection = temporalite.connect('abcd')
>>> connection.execute('CREATE TABLE boopboop (id INT PRIMARY KEY NOT NULL)')
```

Database file gets created with two tables, `boopboop` and `boopboop_temporal`

```
sqlite> .table
boopboop           boopboop_temporal
sqlite> .schema
CREATE TABLE boopboop (id int primary key not null);
CREATE TABLE boopboop_temporal (id int, valid_from date, valid_to date);
```

### Insert Query

New rows get created in temporal table on every new row added in normal table.

```
>>> connection.execute('INSERT INTO boopboop VALUES (100)')
>>> connection.execute('INSERT INTO boopboop VALUES (150)')
```

```
sqlite> select * from boopboop;
100
150
sqlite> select * from boopboop_temporal;
100|1-11-2018|
150|1-11-2018|
```

### Select Query

#####  Nopie nope

### Update Query

### Delete Query

#####  Nopie nope
