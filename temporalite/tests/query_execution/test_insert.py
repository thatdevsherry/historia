# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import sqlite3
import datetime
import subprocess

from temporalite.intercept.insert import InsertQueryBuilder
from temporalite.query_execution.insert import InsertQuery


def setup_module():
    connection = sqlite3.connect('test_file')
    connection.execute("create table test (id int, name text)")
    connection.execute(
        "create table test_history (id int, name text, valid_from datetime, valid_to datetime)"
    )


def teardown_module():
    subprocess.call(["rm", "test_file"])


def test_insert_execution():
    test_query = "insert into test values (1, 'sherry')"
    connection = sqlite3.connect('test_file')
    query_info = InsertQueryBuilder(test_query,
                                    datetime.datetime.now().isoformat())
    assert None is InsertQuery.execute(connection, query_info)
