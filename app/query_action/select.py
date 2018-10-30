# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import sqlite3


class SelectQuery:
    def perform_query_action(basic_keywords, temporal_keywords):
        SelectQuery.perform_basic_keywords_action(basic_keywords)
        SelectQuery.perform_temporal_keywords_action(temporal_keywords)

    def perform_basic_keywords_action(basic_keywords):
        pass

    def perform_temporal_keywords_action(temporal_keywords):
        pass
