# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from app.constants import temporal_keywords_list


class SyntaxConstraintsCheck:
    """
    For more information about these checks, see
    3. Preliminaries -> 1. Definition -> syntax constraints in
    https://dl.comp.nus.edu.sg/bitstream/handle/1900.100/6906/TRA3_18.pdf
    """

    def __init__(self, temporal_keywords):

        self.temporal_keywords = temporal_keywords

        self.check_keywords(temporal_keywords)
        self.check_time_period_adjacent_to_temporal_predicate(
            temporal_keywords)
        self.check_temporal_predicate(temporal_keywords)
        self.get_temporal_keywords(temporal_keywords)

    def check_keywords(self, temporal_keywords):
        for word in temporal_keywords_list:
            if word in temporal_keywords[0] and word in temporal_keywords[-1]:
                raise Exception(
                    "Temporal predicate cannot be in the start or end.")

    def check_time_period_adjacent_to_temporal_predicate(
            self, temporal_keywords):
        pass

    def check_temporal_predicate(self, temporal_keywords):
        pass

    def get_temporal_keywords(self, temporal_keywords):
        for word in temporal_keywords_list:
            if word in temporal_keywords:
                self.temporal_keywords = temporal_keywords[temporal_keywords.
                                                           index(word):]
