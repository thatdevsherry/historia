# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>

# TODO: Use regular expressions for the methods
import re


class QueryParser:
    def __init__(self, query):
        self.query = str.lower(query)

    def get_sql_keywords(self):
        pass

    def get_temporal_keywords(self):
        pass

    def has_temporal_keywords(self):
        temporal_keywords_pattern = re.compile(
            r'(as of|contained in|to|between|and)')

        temporal_keywords_match = temporal_keywords_pattern.finditer(
            self.query)

        keyword_match = None

        for match in temporal_keywords_match:
            keyword_match = match

        if keyword_match is not None:
            return True
        else:
            return False

    def has_temporal_predicate(self):
        pass

    def has_time_period(self):
        pass

    def has_time_point(self):
        pass
