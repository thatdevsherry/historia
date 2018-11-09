# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import sqlite3
import datetime
import subprocess

from temporalite.intercept.select import TemporalSelectQueryBuilder
from temporalite.query_execution.select import (NormalSelectQuery,
                                                TemporalSelectQuery)


def setup_module():
    connection = sqlite3.connect('test_file')
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
    temporal_query_execute = TemporalSelectQuery.execute(
        connection, query_info)
    assert isinstance(temporal_query_execute, sqlite3.Cursor)
