# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>


class SyntaxConstraintsCheck:
    def __init__(self, temporal_keywords):

        self.temporal_keywords = temporal_keywords
        self.check_keywords(temporal_keywords)
        self.check_time_period_adjacent_to_temporal_predicate(
            temporal_keywords)
        self.check_temporal_predicate(temporal_keywords)

    def check_keywords(self, temporal_keywords):
        pass

    def check_time_period_adjacent_to_temporal_predicate(
            self, temporal_keywords):
        pass

    def check_temporal_predicate(self, temporal_keywords):
        pass
