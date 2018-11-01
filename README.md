# temporalite (In Active Development)
A Python module which aims to implement temporal databases by using python's built-in sqlite3 module.


## Status

### Create Query

Able to create tables.

```
>>> import temporalite
>>> connection = temporalite.connect('abcd')
>>> connection.execute("CREATE TABLE test (id INT PRIMARY KEY NOT NULL, name TEXT)")
```

Database file gets created with two tables, `test` and `test_temporal`

```
sqlite> .table
test           test_temporal
sqlite> .schema
CREATE TABLE test (id int primary key not null, name text);
CREATE TABLE test_temporal (id int not null, name text, valid_from date, valid_to date);
```

### Insert Query

New rows get created in temporal table on every new row added in normal table.

```
>>> connection.execute("INSERT INTO test VALUES (1, 'sherry')")
>>> connection.commit()
```

```
sqlite> select * from test;
1|sherry
sqlite> select * from test_temporal;
1|sherry|1-11-2018|
```

### Update Query

Works but has limitations:

- can only change one column per query
- query must not have spaces in the column_name=new_value

```
>>> connection.execute("UPDATE test SET name='it_changed' WHERE id=1")
>>> connection.commit()
```

```
sqlite> select * from test;
1|it_changed
sqlite> select * from test_temporal;
1|sherry|1-11-2018|1-11-2018
1|it_changed|1-11-2018|
sqlite>
```

### Select Query

#####  Nopie nope

### Delete Query

#####  Nopie nope
