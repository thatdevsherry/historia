# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from temporalite.intercept.insert import InsertQueryBuilder


def test_table_name():
    test_query = "insert into test values (1, 'sherry')"
    builder_object = InsertQueryBuilder(test_query)
    assert builder_object.table_name == "test"


def test_temporal_table_name():
    test_query = "insert into test values (1, 'sherry')"
    builder_object = InsertQueryBuilder(test_query)
    assert builder_object.temporal_table_name == "test_history"


def test_original_query():
    """Make sure original query wasn't altered."""
    test_query = "insert into test values (1, 'sherry')"
    builder_object = InsertQueryBuilder(test_query)
    assert builder_object.query == test_query


def test_get_table_span():
    test_query = "insert into test values (1, 'sherry')"
    assert InsertQueryBuilder.get_table_span(test_query) == (12, 16)


def test_get_after_table_part():
    test_query = "insert into test values (1, 'sherry')"
    builder_object = InsertQueryBuilder(test_query)
    assert " values " == builder_object.get_after_table_part(test_query)


def test_get_values():
    test_query = "insert into test values (1, 'sherry')"
    assert "(1, 'sherry'" == InsertQueryBuilder.get_values(test_query)
