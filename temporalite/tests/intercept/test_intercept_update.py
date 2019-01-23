"""
Copyright (c) 2019 Muhammad Shehriyar Qureshi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
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


def test_create_column_values_list():
    values_string = "name='something',name2='wut'"
    column_value_list = UpdateQueryBuilder.create_column_values_list(
        values_string)
    assert ['name', "'something'", 'name2', "'wut'"] == column_value_list


def test_create_column_value_dictionary():
    column_value_list = ['name', "'something'", 'name2', "'wut'"]
    column_value_dictionary = UpdateQueryBuilder.create_column_value_dictionary(
        column_value_list)
    assert {'name': "'something'", 'name2': "'wut'"} == column_value_dictionary


def test_create_new_query_values():
    time_string = datetime.datetime.now().isoformat()
    test_query = "update test set name='abcd' where id=1"
    connection = sqlite3.connect('test_file')
    builder_object = UpdateQueryBuilder(test_query, connection, time_string)
    column_value_dictionary = {'name': "'something'", 'id': '10'}
    full_row = (1, 'sherry')
    new_query = builder_object.create_new_query_values(column_value_dictionary,
                                                       full_row)
    assert ('10', "'something'") == new_query
