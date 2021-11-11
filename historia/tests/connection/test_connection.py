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
import re
import sqlite3
import subprocess

from historia.connection.connection import Connection

import pytest


def teardown_module():
    subprocess.call(["rm", "test_file"])


def test_connection_path():
    test_connection = Connection("test_file")
    assert test_connection.verify_file_path() is None


def test_connection_file_name():
    test_connection = Connection("test_file")
    assert test_connection.database_file == "test_file"


def test_sqlite_connection():
    test_connection = Connection("test_file")
    assert test_connection.sqlite_connection is not None


def test_invalid_path_to_database_file():
    with pytest.raises(sqlite3.OperationalError):
        Connection("in/valid/file.db")


def test_connection_commit():
    test_connection = Connection("test_file")
    assert test_connection.commit() is None


def test_connection_close():
    test_connection = Connection("test_file")
    assert test_connection.close() is None


def test_create_history_table():
    # setup db
    connection = sqlite3.connect("test_file")
    connection.execute("CREATE TABLE test (id int)")
    connection.execute("CREATE TABLE test_again (id int, something int)")
    connection.close()
    # close setup

    # start test

    test_connection = Connection("test_file")
    test_connection.create_history_tables()
    test_connection.close()

    # should have created history tables for above tables
    connection = sqlite3.connect("test_file")
    query = connection.execute("SELECT sql FROM sqlite_master")
    query_output = query.fetchall()
    history_tables_list = []

    for i in query_output:
        pattern = re.compile("_history")
        matches = pattern.finditer(i[0])

        for match in matches:
            history_tables_list.append(match.group(0))

    assert len(history_tables_list) == 2
