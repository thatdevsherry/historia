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
from temporalite.intercept.select import TemporalSelectQueryBuilder


def test_original_table_name():
    test_query = "select * from test as of '2018T'"
    builder_object = TemporalSelectQueryBuilder(test_query)
    assert "test" == builder_object.table_name


def test_selected_column():
    test_query = "select * from test as of '2018T'"
    builder_object = TemporalSelectQueryBuilder(test_query)
    assert "*" == builder_object.selected_column


def test_temporal_table_name():
    test_query = "select * from test as of '2018T'"
    builder_object = TemporalSelectQueryBuilder(test_query)
    assert "test_history" == builder_object.temporal_table_name


def test_temporal_clause():
    test_query = "select * from test as of '2018T'"
    builder_object = TemporalSelectQueryBuilder(test_query)
    assert "as of" == builder_object.temporal_clause


def test_build_as_of_temporal_query():
    test_query = "select * from test as of '2018T'"
    builder_object = TemporalSelectQueryBuilder(test_query)
    assert "select * from test_history where valid_from <= '2018T' and valid_to > '2018T'" == builder_object.temporal_query


def test_build_between_and_temporal_query():
    test_query = "select * from test between '2018T' and '2019T'"
    builder_object = TemporalSelectQueryBuilder(test_query)
    assert "select * from test_history where valid_from <= '2019T' and valid_to > '2018T'" == builder_object.temporal_query


def test_build_contained_in_temporal_query():
    test_query = "select * from test contained in('2018T', '2019T')"
    builder_object = TemporalSelectQueryBuilder(test_query)
    assert "select * from test_history where valid_from >= '2018T' and valid_to <= '2019T'" == builder_object.temporal_query


def test_build_from_to_temporal_query():
    test_query = "select * from test contained in('2018T', '2019T')"
    builder_object = TemporalSelectQueryBuilder(test_query)
    assert "select * from test_history where valid_from >= '2018T' and valid_to <= '2019T'" == builder_object.temporal_query
