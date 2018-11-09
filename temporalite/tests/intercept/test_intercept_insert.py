# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import time
import datetime

from temporalite.intercept.insert import InsertQueryBuilder


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
