# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import re

from pudb import set_trace


class SelectQueryHandler:
    def is_temporal_query(parsed_query):
        set_trace()
        original_query = ' '.join(parsed_query)

        # will add more clauses as they're implemented
        temporal_clause_pattern = re.compile(r'(as of )')

        temporal_clause_matches = temporal_clause_pattern.finditer(
            original_query)

        temporal_clause_match = None

        for match in temporal_clause_matches:
            temporal_clause_match = match

        if temporal_clause_match is not None:
            return True

        else:
            return False
