# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from app.intercept.create import CreateTableQuery


class QueryActionInfo:
    def decide_action(parsed_query):
        if parsed_query.query[0] == "create":
            return CreateTableQuery(parsed_query)
