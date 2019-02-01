# Historia
A Python module which implements temporal tables using python's built-in sqlite3 module.


## What is it?

Consider you have a database of employees. One of em pretends to be a "Me Me Big Boy" but is actually a smol boi. You fire him. That's right. So you delete his record (row) from database. 1 year later you find out he was doing
some shady stuff behind your back and police are after him. They come to you to get his information. So you query the database with his ID and... ummm... well this is embarrassing. You deleted the row so uh... it's gone... you look
at the officer's face and he thinks you're one of those IT people that think they can do stuff but actually can't. The officer says "degrees are useless". You drown in disappointment.

That's where history tables come in. They keep track of what happened in the database, what got changed and when it got changed. They can be useful for restoring data if database goes corrupt or be used for audit purposes. Support
for temporal tables is in most databases. I just wanted a project to work on so I decided to implement (with my current knowledge) temporal tables using python's built-in sqlite3 module.


## How it works (Simple Edition)

The only part it does itself is the parsing and creation of temporal queries. The connection and execute functions just call the sqlite3 functions. It's like that kid that copies others work and pretends he did it.

### Table Creation

You enter a query to create a table. The module looks in disgust on how bad you named the table and columns. It then creates another table (the history one) with two additional columns, **valid_from** and **valid_to**.

### Manipulation

When you enter queries for inserting/updating or deleting, it automatically parses your query and creates a temporal query from it and executes both of them using python's sqlite3 module. (I'm saying this quite often now)

### Fetching

When you enter a select statement, it looks if you used a temporal clause like AS OF. If you don't, it runs the normal query and gives you the result from temporal table (current/NOT THE HISTORY ONE). If you do enter a temporal
clause, it parses it and uses really complicated equations e.g. (a > b AND b < c) and returns the result from history_table.

## Status

### Create Query

Able to create tables.

```
>>> import historia
>>> connection = historia.connect('abcd')
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
1|sherry|2018-11-06T15:02:40.079655|9999-12-31T00:00:00.000000
```

### Update Query

```
>>> connection.execute("UPDATE test SET name='it_changed' WHERE id=1")
>>> connection.commit()
```

```
sqlite> select * from test;
1|it_changed
sqlite> select * from test_history;
1|sherry|2018-11-06T15:02:40.079655|2018-11-06T15:03:22.911268
1|it_changed|2018-11-06T15:03:22.911268|9999-12-31T00:00:00.000000
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
1|sherry|2018-11-06T15:02:40.079655|2018-11-06T15:03:22.911268
1|it_changed|2018-11-06T15:03:22.911268|2018-11-06T15:03:49.029362
```

### Select Query

These queries work by following the conditions defined in https://docs.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables?view=sql-server-2017#how-do-i-query-temporal-data

#### NOTE: These only perform queries on history table for now.

Will add support for returning **temporal_table UNION history_table** result when possible.

Supported clauses:

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
