# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from app.constants import temporal_keywords


class QueryParser:
    def __init__(self, query, is_temporal_query=None):
        self.query = tuple(str.lower(query).split(" "))
        self.is_temporal_query = is_temporal_query

    def get_basic_keywords(self):
        pass

    def get_temporal_keywords(self):
        pass

    def has_temporal_keywords(self):
        for word in self.query:
            if word in temporal_keywords:
                self.is_temporal_query = True
