# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from temporalite.intercept.create import CreateQueryBuilder


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
