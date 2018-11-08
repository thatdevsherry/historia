# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>

# TODO: Use regular expressions for the methods


class QueryParser:
    def __init__(self, query):
        self.query = tuple(str.lower(query).split(" "))

    def get_sql_keywords(self):
        pass

    def get_temporal_keywords(self):
        pass

    def has_temporal_keywords(self):
        pass

    def has_temporal_predicate(self):
        pass

    def has_time_period(self):
        pass

    def has_time_point(self):
        pass
