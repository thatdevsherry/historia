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
from historia.intercept.create import CreateQueryBuilder


def setup_module():
    pass


def teardown_module():
    pass


def test_original_table_name():
    test_query = "create table test (id int, name text)"
    query_object = CreateQueryBuilder(test_query)
    assert query_object.table_name == "test"


def test_temporal_table_name():
    test_query = "create table test (id int, name text)"
    query_object = CreateQueryBuilder(test_query)
    assert query_object.temporal_table_name == "test_history"


def test_query():
    '''Make sure original query is not altered in any way.'''
    test_query = "create table test (id int, name text)"
    query_object = CreateQueryBuilder(test_query)
    assert query_object.query == test_query


def test_temporal_query():
    test_query = "create table test (id int, name text)"
    query_object = CreateQueryBuilder(test_query)
    assert query_object.temporal_query == "create table test_history (id int, name text, valid_from datetime, valid_to datetime)"


def test_temporal_column():
    test_query = "create table test (id int, name text)"
    columns_string = CreateQueryBuilder.build_temporal_columns(test_query)
    assert "(id int, name text, valid_from datetime, valid_to datetime)" == columns_string


def test_get_table_part():
    test_query = "create table test (id int, name text)"
    table_part = CreateQueryBuilder.get_table_part(test_query)
    assert "create table " == table_part


def test_primary_key_strip():
    test_query = "create table test (id int, name text)"
    without_primary_key = CreateQueryBuilder.without_primary_key(
        "(id int, name text, valid_from datetime, valid_to datetime)")
