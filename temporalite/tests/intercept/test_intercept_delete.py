# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
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
