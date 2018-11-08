# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import sqlite3
import subprocess

from temporalite.connection.connection import Connection

import pytest


def teardown_module():
    subprocess.call(["rm", "test_file"])


def test_connection_path():
    test_connection = Connection('test_file')
    assert test_connection.verify_file_path() is None


def test_connection_file_name():
    test_connection = Connection('test_file')
    assert test_connection.database_file == 'test_file'


def test_sqlite_connection():
    test_connection = Connection('test_file')
    assert test_connection.sqlite_connection is not None


def test_invalid_path_to_database_file():
    with pytest.raises(sqlite3.OperationalError):
        Connection('in/valid/file.db')


def test_connection_commit():
    test_connection = Connection('test_file')
    assert test_connection.commit() is None


def test_connection_close():
    test_connection = Connection('test_file')
    assert test_connection.close() is None
