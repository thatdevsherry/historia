# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import sqlite3


class CreateQuery:
    def execute(connection, query_info):
        try:
            connection.execute(query_info.query)
        except sqlite3.OperationalError:
            pass
        # perform temporal query
        connection.execute(query_info.temporal_query)
