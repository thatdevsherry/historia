# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail>
import sqlite3
import datetime
import subprocess

from temporalite.intercept.delete import DeleteQueryBuilder
from temporalite.query_execution.delete import DeleteQuery


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


def test_delete_query_execution():
    test_query = "delete from test where id=1"
    connection = sqlite3.connect("test_file")
    query_info = DeleteQueryBuilder(test_query,
                                    datetime.datetime.now().isoformat())
    assert None is DeleteQuery.execute(connection, query_info)
