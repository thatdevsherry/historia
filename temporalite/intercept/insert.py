"""
Copyright (c) 2019 Muhammad Shehriyar Qureshi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re
import datetime


class InsertQueryBuilder:
    def __init__(self,
                 query,
                 local_time,
                 table_name=None,
                 temporal_table_name=None,
                 temporal_query=None):
        self.query = query
        self.local_time = local_time
        self.table_name = table_name
        self.temporal_table_name = temporal_table_name
        self.temporal_query = temporal_query

        self.set_table_names()
        self.build_temporal_query(local_time)

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

    def build_temporal_query(self, time_string):
        original_query = self.query

        table_name_span = InsertQueryBuilder.get_table_span(original_query)

        # get string before table name
        before_table = original_query[:table_name_span[0]]

        after_table_before_values = InsertQueryBuilder.get_after_table_part(
            self, original_query)

        values = InsertQueryBuilder.get_values(original_query)

        # this string will be cocatenated in the end position
        # it adds the temporal time column values and closing bracket
        add_values = "{}, '{}', '9999-12-31T00:00:00.000000')".format(
            values, time_string)

        self.temporal_query = before_table + self.temporal_table_name + \
            after_table_before_values + add_values
