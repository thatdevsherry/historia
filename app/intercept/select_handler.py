# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from app.constants import select_temporal_keywords


class SelectQueryHandler:
    def is_temporal_query(parsed_query):
        for word in parsed_query:
            if word in select_temporal_keywords:
                return True

        return False
