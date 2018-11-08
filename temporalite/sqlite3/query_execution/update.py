# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>


class UpdateQuery:
    def execute(connection, query_info):
        # execute user_query
        connection.execute(query_info.query.query)
        # update temporal row
        connection.execute(query_info.temporal_query)
        # insert new row in temporal table
        connection.execute(query_info.temporal_query_insert)
