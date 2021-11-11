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

from historia.intercept.select import TemporalSelectQueryBuilder
from historia.query_execution.select import NormalSelectQuery, TemporalSelectQuery


def setup_module():
    connection = sqlite3.connect("test_file")
    connection.execute("create table test (id int, name text)")
    connection.execute(
        "create table test_history (id int, name text, valid_from datetime, valid_to datetime)"
    )
    connection.execute("insert into test values (1, 'sherry')")
    connection.commit()


def teardown_module():
    subprocess.call(["rm", "test_file"])


def test_normal_query_execution():
    test_query = "select * from test"
    connection = sqlite3.connect("test_file")
    normal_query_execute = NormalSelectQuery.execute(connection, test_query)
    assert isinstance(normal_query_execute, sqlite3.Cursor)


def test_temporal_execution_returns_cursor_object():
    test_query = "select * from test as of '2018-11-11T00:00:00.000000'"
    query_info = TemporalSelectQueryBuilder(test_query)
    connection = sqlite3.connect("test_file")
    temporal_query_execute = TemporalSelectQuery.execute(connection, query_info)
    assert isinstance(temporal_query_execute, sqlite3.Cursor)
