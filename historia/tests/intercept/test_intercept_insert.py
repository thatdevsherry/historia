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
import time
import datetime

from historia.intercept.insert import InsertQueryBuilder


def test_table_name():
    test_query = "insert into test values (1, 'sherry')"
    builder_object = InsertQueryBuilder(test_query,
                                        datetime.datetime.now().isoformat())
    assert builder_object.table_name == "test"


def test_temporal_table_name():
    test_query = "insert into test values (1, 'sherry')"
    builder_object = InsertQueryBuilder(test_query,
                                        datetime.datetime.now().isoformat())
    assert builder_object.temporal_table_name == "test_history"


def test_original_query():
    """Make sure original query wasn't altered."""
    test_query = "insert into test values (1, 'sherry')"
    builder_object = InsertQueryBuilder(test_query,
                                        datetime.datetime.now().isoformat())
    assert builder_object.query == test_query


def test_get_table_span():
    test_query = "insert into test values (1, 'sherry')"
    assert InsertQueryBuilder.get_table_span(test_query)


def test_get_after_table_part():
    test_query = "insert into test values (1, 'sherry')"
    builder_object = InsertQueryBuilder(test_query,
                                        datetime.datetime.now().isoformat())
    assert " values " == builder_object.get_after_table_part(test_query)


def test_get_values():
    test_query = "insert into test values (1, 'sherry')"
    assert "(1, 'sherry'" == InsertQueryBuilder.get_values(test_query)


def test_build_temporal_query():
    time_string = datetime.datetime.now().isoformat()
    test_query = "insert into test values (1, 'sherry')"
    builder_object = InsertQueryBuilder(test_query, time_string)
    print(builder_object.temporal_query)
    assert "insert into test_history values (1, 'sherry', '{}', '9999-12-31T00:00:00.000000')".format(
        time_string) == builder_object.temporal_query
