# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import sqlite3
import datetime
import subprocess

from temporalite.intercept.update import UpdateQueryBuilder
from temporalite.query_execution.update import UpdateQuery


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


def test_update_query_execution():
    test_query = "update test set name='something' where id=1"
    connection = sqlite3.connect("test_file")
    query_info = UpdateQueryBuilder(test_query, connection,
                                    datetime.datetime.now().isoformat())
    assert None is UpdateQuery.execute(connection, query_info)
