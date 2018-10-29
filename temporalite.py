# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from app.parser.QueryParser import QueryParser


def main_execution(args):
    parsed_query = QueryParser(args)
    basic_keywords = parsed_query.get_basic_keywords()
    temporal_keywords = parsed_query.get_temporal_keywords()
    return parsed_query


if "__name__" == "__main__":
    main_execution(*args)
