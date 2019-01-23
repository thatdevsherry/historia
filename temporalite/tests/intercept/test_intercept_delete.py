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
import datetime

from temporalite.intercept.delete import DeleteQueryBuilder


def test_original_table_name():
    test_query = "delete from test where id=1"
    builder_object = DeleteQueryBuilder(test_query,
                                        datetime.datetime.now().isoformat())
    assert builder_object.table_name == "test"


def test_temporal_table_name():
    test_query = "delete from test where id=1"
    builder_object = DeleteQueryBuilder(test_query,
                                        datetime.datetime.now().isoformat())
    assert builder_object.temporal_table_name == "test_history"


def test_query():
    '''Make sure original query wasn't altered.'''
    test_query = "delete from test where id=1"
    builder_object = DeleteQueryBuilder(test_query,
                                        datetime.datetime.now().isoformat())
    assert builder_object.query == test_query


def test_where_condition():
    test_query = "delete from test where id=1"
    assert DeleteQueryBuilder.get_where_condition(test_query) == "id=1"


def test_temporal_query():
    local_time = datetime.datetime.now().isoformat()
    test_query = "delete from test where id=1"
    builder_object = DeleteQueryBuilder(test_query, local_time)
    assert "update test_history set valid_to='{}' where id=1 and valid_to='9999-12-31T00:00:00.000000'".format(
        local_time) == builder_object.temporal_query
