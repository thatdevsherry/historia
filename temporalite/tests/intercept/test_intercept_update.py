# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import sqlite3
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
    builder_object = UpdateQueryBuilder(test_query, connection)
    assert "test" == builder_object.table_name


def test_temporal_table_name():
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection)
    assert "test_history" == builder_object.temporal_table_name


def test_get_update_column():
    test_query = "update test set name='abcd' where id=1"
    assert "name" == UpdateQueryBuilder.get_update_column(test_query)


def test_full_row():
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection)
    builder_object.get_full_row("id=1")
    assert (1, 'sherry') == builder_object.get_full_row("id=1")


def test_get_new_values():
    test_query = "update test set name='abcd' where id=1"
    assert "name='abcd'" == UpdateQueryBuilder.get_new_values(test_query)


def test_get_only_column_value():
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection)
    assert "sherry" == builder_object.get_only_column_value("id=1", "name")
