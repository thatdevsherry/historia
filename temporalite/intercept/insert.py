# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import re
import datetime


class InsertQueryBuilder:
    def __init__(self,
                 query,
                 table_name=None,
                 temporal_table_name=None,
                 temporal_query=None):
        self.query = query
        self.table_name = table_name
        self.temporal_table_name = temporal_table_name
        self.temporal_query = temporal_query

        self.set_table_names()
        self.build_temporal_query()

    def set_table_names(self):
        InsertQueryBuilder.set_original_table_name(self)
        InsertQueryBuilder.set_temporal_table_name(self)

    def set_original_table_name(self):
        original_query = self.query
        table_name_pattern = re.compile(r'(?<=into )(.*)(?= values)')

        matches = table_name_pattern.finditer(original_query)

        for match in matches:
            table_name_match = match

        self.table_name = table_name_match.group(0)

    def get_table_span(original_query):
        table_name_pattern = re.compile(r'(?<=into )(.*)(?= values)')

        matches = table_name_pattern.finditer(original_query)

        for match in matches:
            table_name_match = match

        table_name_span = table_name_match.span()
        return table_name_span

    def set_temporal_table_name(self):
        self.temporal_table_name = self.table_name + "_history"

    def get_after_table_part(self, original_query):
        # get values b/w table and opening bracket '(' of values
        keyword_values_pattern = re.compile(r'(?<={})(.*)(?=\()'.format(
            self.table_name))

        keyword_values_matches = keyword_values_pattern.finditer(
            original_query)

        for match in keyword_values_matches:
            keyword_values_match = match

        after_table_before_values = keyword_values_match.group(0)
        return after_table_before_values

    def get_values(original_query):
        values_pattern = re.compile(r'\((.*)(?=\))')

        values_matches = values_pattern.finditer(original_query)

        for match in values_matches:
            values_match = match

        values = values_match.group(0)
        return values

    def build_temporal_query(self):
        original_query = self.query

        table_name_span = InsertQueryBuilder.get_table_span(original_query)

        # get string before table name
        before_table = original_query[:table_name_span[0]]

        after_table_before_values = InsertQueryBuilder.get_after_table_part(
            self, original_query)

        values = InsertQueryBuilder.get_values(original_query)

        time_string = datetime.datetime.now().isoformat()

        # this string will be cocatenated in the end position
        # it adds the temporal time column values and closing bracket
        add_values = "{}, '{}', '9999-12-31T00:00:00.000000')".format(
            values, time_string)

        self.temporal_query = before_table + self.temporal_table_name + \
            after_table_before_values + add_values
