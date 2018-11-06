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

Database file gets created with two tables, `test` and `test_history`

```
sqlite> .table
test           test_history
sqlite> .schema
CREATE TABLE test (id int primary key not null, name text);
CREATE TABLE test_history (id int not null, name text, valid_from date, valid_to date);
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
sqlite> select * from test_history;
1|sherry|2018-11-02T23:21:36.245275|9999-12-31T00:00:00.000000
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
1|something
sqlite> select * from test_history;
1|sherry|2018-11-02T23:21:36.245275|2018-11-02T23:22:36.631443
1|something|2018-11-02T23:22:36.632108|9999-12-31T00:00:00.000000
```

### Delete Query

```
>>> connection.execute("DELETE FROM test WHERE id=1")
>>> connection.commit()
```

Database:

```
sqlite> select * from test;
sqlite> select * from test_history;
1|sherry|2018-11-02T23:21:36.245275|2018-11-02T23:23:22.888240
1|something|2018-11-02T23:22:36.632108|2018-11-02T23:23:22.888240
```

### Select Query

Working clauses:

- **AS OF**

```
select * from test as of '2018-11-05T15:00:00.000000'
```

- **FROM 'X' TO 'Z'**

```
select * from test from '2018-11-05T09:00:00.000000' to '2018-11-06T12:00:00.000000'
```

- **BETWEEN 'X' AND 'Z'**

```
select * from test between '2018-11-05T12:00:00.000000' and '2018-11-06T09:00:00.000000'
```

- **CONTAINED IN ('X', 'Y')**

```
select * from test contained in ('2018-11-05T12:00:00.000000', '2018-11-06T10:00:00.000000')
```
