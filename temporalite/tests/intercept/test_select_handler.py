# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
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
