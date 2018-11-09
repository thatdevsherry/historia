# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>


class NormalSelectQuery:
    def execute(connection, query):
        return connection.execute(query)


class TemporalSelectQuery:
    def execute(connection, query_info):
        return connection.execute(query_info.temporal_query)
