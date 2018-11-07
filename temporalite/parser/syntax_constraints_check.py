# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from ..constants.constants import temporal_keywords_list


class SyntaxConstraintsCheck:
    """
    For more information about these checks, see
    3. Preliminaries -> 1. Definition -> syntax constraints in
    https://dl.comp.nus.edu.sg/bitstream/handle/1900.100/6906/TRA3_18.pdf
    """

    def __init__(self, query):

        self.query = query

        self.check_keywords(query)
        self.check_time_period_adjacent_to_temporal_predicate(query)
        self.check_temporal_predicate(query)
        self.get_temporal_keywords(query)

    def check_keywords(self, query):
        for word in temporal_keywords_list:
            if word in query[0] and word in query[-1]:
                raise Exception(
                    "Temporal predicate cannot be in the start or end.")

    def check_time_period_adjacent_to_temporal_predicate(self, query):
        pass

    def check_temporal_predicate(self, query):
        pass

    def get_temporal_keywords(self, query):
        for word in temporal_keywords_list:
            if word in query:
                self.query = query[query.index(word):]
