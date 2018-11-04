# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import re
import datetime


class InsertQueryBuilder:
    def __init__(self, query, temporal_query=None):
        self.query = query
        self.temporal_query = temporal_query

        self.build_temporal_query()

    def build_temporal_query(self):
        original_query = ' '.join(self.query.query)

        # get table name
        table_name_pattern = re.compile(r'(?<=into )(.*)(?= values)')

        matches = table_name_pattern.finditer(original_query)

        for match in matches:
            table_name_match = match

        table_name_span = table_name_match.span()
        table_name = table_name_match.group(0)

        temporal_table = table_name + "_history"

        # get string before table name
        before_table = original_query[:table_name_span[0]]

        # get values b/w table and opening bracket '(' of values
        keyword_values_pattern = re.compile(
            r'(?<={})(.*)(?=\()'.format(table_name))

        keyword_values_matches = keyword_values_pattern.finditer(
            original_query)

        for match in keyword_values_matches:
            keyword_values_match = match

        after_table_before_values = keyword_values_match.group(0)

        # get values inside brackets
        values_pattern = re.compile(r'\((.*)(?=\))')

        values_matches = values_pattern.finditer(original_query)

        for match in values_matches:
            values_match = match

        values = values_match.group(0)

        time_string = datetime.datetime.now().isoformat()

        # this string will be cocatenated in the end position
        # it adds the temporal time column values and closing bracket
        add_values = "{}, '{}', '9999-12-31T:00:00:00.000000')".format(
            values, time_string)

        self.temporal_query = before_table + temporal_table + \
            after_table_before_values + add_values
