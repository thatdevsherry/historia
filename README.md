# temporalite (In Active Development)
A Python module which aims to implement temporal databases by using python's built-in sqlite3 module.


## Status

### Create Query

Able to create tables.

```
import temporalite
connection = temporalite.connect('abcd')
connection.execute("CREATE TABLE boopboop (id INT PRIMARY KEY NOT NULL, name TEXT NOT NULL)")
```

Database file gets created with two tables, `boopboop` and `boopboop_temporal`

```
sqlite> .table
boopboop           boopboop_temporal
sqlite> .schema
CREATE TABLE boopboop (id int primary key not null, name text not null);
CREATE TABLE boopboop_temporal (id int primary key not null, name text not null, valid_from date, valid_to date);
```


### Insert Query


#####  Nopie nope


### Select Query

#####  Nopie nope

### Update Query

#####  Nopie nope

### Delete Query

#####  Nopie nope
