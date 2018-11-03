# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>


class NormalSelectQuery:
    def execute(connection, parsed_query):
        return connection.execute(' '.join(parsed_query))


class TemporalSelectQuery:
    pass
