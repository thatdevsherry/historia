# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import re


class CreateQueryBuilder:
    def __init__(self,
                 query,
                 temporal_query=None,
                 table_name=None,
                 temporal_table_name=None):
        self.query = query
        self.temporal_query = temporal_query
        self.table_name = table_name
        self.temporal_table_name = temporal_table_name

        self.set_table_names()
        self.build_temporal_query()

    def set_original_table_name(self):
        # convert query tuple to string
        original_query = ' '.join(self.query.query)
        get_table_pattern = re.compile(r'(?<=table )(.*)(?= \()')

        matches = get_table_pattern.finditer(original_query)

        for match in matches:
            table_name_match = match

        table_name_span = table_name_match.span()
        self.table_name = original_query[table_name_span[0]:table_name_span[1]]

    def set_temporal_table_name(self):
        self.temporal_table_name = self.table_name + "_history"

    def set_table_names(self):
        CreateQueryBuilder.set_original_table_name(self)
        CreateQueryBuilder.set_temporal_table_name(self)

    def build_temporal_query(self):
        # convert query tuple to string
        original_query = ' '.join(self.query.query)
        get_columns_pattern = re.compile(r'\([^)]+\w')

        matches = get_columns_pattern.finditer(original_query)

        for match in matches:
            columns = match.group(0)

        new_columns_string = columns + ", valid_from datetime, valid_to datetime)"

        get_table_pattern = re.compile(r'(?<=table )(.*)(?= \()')

        another_match = get_table_pattern.finditer(original_query)

        for match in another_match:
            table_names = match

        table_name_span = table_names.span()
        table_part = original_query[:table_name_span[0]]

        primary_key_pattern = re.compile(r' primary key')

        primary_keys = primary_key_pattern.finditer(new_columns_string)

        key_span = None

        for match in primary_keys:
            key_span = match.span()

        if key_span is not None:

            before_key = new_columns_string[:key_span[0]]
            after_key = new_columns_string[key_span[1]:]
            self.temporal_query = table_part + \
                self.temporal_table_name + " " + before_key + after_key

        else:
            self.temporal_query = table_part + \
                self.temporal_table_name + " " + new_columns_string
