# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import sqlite3
import datetime
import subprocess

from temporalite.intercept.update import UpdateQueryBuilder


def setup_module():
    connection = sqlite3.connect('test_file')
    connection.execute("create table test (id int, name text)")
    connection.execute("insert into test values (1, 'sherry')")
    connection.commit()


def teardown_module():
    subprocess.call(["rm", "test_file"])


def test_original_table_name():
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection,
                                        datetime.datetime.now().isoformat())
    assert "test" == builder_object.table_name


def test_temporal_table_name():
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection,
                                        datetime.datetime.now().isoformat())
    assert "test_history" == builder_object.temporal_table_name


def test_get_update_column():
    test_query = "update test set name='abcd' where id=1"
    assert "name" == UpdateQueryBuilder.get_update_column(test_query)


def test_full_row():
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection,
                                        datetime.datetime.now().isoformat())
    builder_object.get_full_row("id=1")
    assert (1, 'sherry') == builder_object.get_full_row("id=1")


def test_get_new_values():
    test_query = "update test set name='abcd' where id=1"
    assert "name='abcd'" == UpdateQueryBuilder.get_new_values(test_query)


def test_get_only_column_value():
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection,
                                        datetime.datetime.now().isoformat())
    assert "sherry" == builder_object.get_only_column_value("id=1", "name")


def test_query():
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection,
                                        datetime.datetime.now().isoformat())
    assert test_query == builder_object.query


def test_temporal_query():
    time_string = datetime.datetime.now().isoformat()
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection, time_string)
    assert "update test_history set valid_to='{}' where id=1 and valid_to='9999-12-31T00:00:00.000000'".format(
        time_string) == builder_object.temporal_query


def test_temporal_query_insert():
    time_string = datetime.datetime.now().isoformat()
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection, time_string)
    assert "insert into test_history values (1, 'abcd', '{}', '9999-12-31T00:00:00.000000')".format(
        time_string) == builder_object.temporal_query_insert
