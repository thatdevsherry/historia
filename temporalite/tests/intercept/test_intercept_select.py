# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
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
