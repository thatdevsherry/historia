# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>


class DeleteQuery:
    def execute(connection, query_info):
        # execute normal query
        connection.execute(query_info.query.query)
        # execute temporal table query
        connection.execute(query_info.temporal_query)
