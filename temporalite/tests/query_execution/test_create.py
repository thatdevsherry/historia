# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail>
import sqlite3
import subprocess

from temporalite.intercept.create import CreateQueryBuilder
from temporalite.query_execution.create import CreateQuery


def teardown_module():
    subprocess.call(["rm", "test_file"])


def test_execute():
    query = "create table test (id int, name text)"
    connection = sqlite3.connect('test_file')
    query_info = CreateQueryBuilder(query)
    assert None is CreateQuery.execute(connection, query_info)
