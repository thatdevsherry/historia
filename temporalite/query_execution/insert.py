# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>


class InsertQuery:
    def execute(connection, query_info):
        connection.execute(query_info.query)
        # perform temporal query
        connection.execute(query_info.temporal_query)
        connection.commit()