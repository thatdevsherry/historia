# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from app.constants import temporal_keywords_list, temporal_predicates_list
from app.parser.syntax_constraints_check import SyntaxConstraintsCheck


class QueryParser:
    def __init__(self, query):
        self.query = tuple(str.lower(query).split(" "))

    def get_basic_keywords(self):
        for word in temporal_keywords:
            if word in self.query:
                return self.query[:self.query.index(word)]

    def get_temporal_keywords(self):
        for word in temporal_keywords:
            if word in self.query:
                return SyntaxConstraintsCheck(self.query).temporal_keywords

    def has_temporal_keywords(self):
        for word in temporal_keywords:
            if word in self.query:
                return True
            else:
                return False

    def has_temporal_predicate(self):
        for word in temporal_predicates_list:
            if word in self.query:
                return True
            else:
                return False

    def has_time_period(self):
        pass

    def has_time_point(self):
        pass
