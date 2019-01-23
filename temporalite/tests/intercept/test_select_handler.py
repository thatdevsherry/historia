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
from temporalite.intercept.select_handler import SelectQueryHandler


def test_is_temporal_query_with_no_keywords_false():
    is_temporal = SelectQueryHandler.is_temporal_query("select * from test")
    assert False is is_temporal


def test_is_temporal_query_with_as_of():
    is_temporal = SelectQueryHandler.is_temporal_query(
        "select * from test as of '9999-12-31T00:00:00.000000'")
    assert True is is_temporal


def test_is_temporal_query_with_from_to():
    is_temporal = SelectQueryHandler.is_temporal_query(
        "select * from test from '9999-12-31T00:00:00.000000' to '9999-12-31T00:00:00.000000'"
    )
    assert True is is_temporal


def test_is_temporal_query_with_between_and():
    is_temporal = SelectQueryHandler.is_temporal_query(
        "select * from test between '9999-12-31T00:00:00.000000' and '9999-12-31T00:00:00.000000'"
    )
    assert True is is_temporal


def test_is_temporal_query_with_contained_in():
    is_temporal = SelectQueryHandler.is_temporal_query(
        "select * from test contained in ('9999-12-31T00:00:00.000000', '9999-12-31T00:00:00.000000')"
    )
    assert True is is_temporal
