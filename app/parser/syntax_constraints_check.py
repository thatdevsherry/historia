# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from app.constants import temporal_keywords_list


class SyntaxConstraintsCheck:
    """
    For more information about these checks, see
    3. Preliminaries -> 1. Definition -> syntax constraints in
    https://dl.comp.nus.edu.sg/bitstream/handle/1900.100/6906/TRA3_18.pdf
    """

    def __init__(self, query_tuple):

        self.query_tuple = query_tuple

        self.check_keywords(query_tuple)
        self.check_time_period_adjacent_to_temporal_predicate(query_tuple)
        self.check_temporal_predicate(query_tuple)
        self.get_temporal_keywords(query_tuple)

    def check_keywords(self, query_tuple):
        for word in temporal_keywords_list:
            if word in query_tuple[0] and word in query_tuple[-1]:
                raise Exception(
                    "Temporal predicate cannot be in the start or end.")

    def check_time_period_adjacent_to_temporal_predicate(self, query_tuple):
        pass

    def check_temporal_predicate(self, query_tuple):
        pass

    def get_temporal_keywords(self, query_tuple):
        for word in temporal_keywords_list:
            if word in query_tuple:
                self.query_tuple = query_tuple[query_tuple.index(word):]
