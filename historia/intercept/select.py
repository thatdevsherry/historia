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


class TemporalSelectQueryBuilder:
    def __init__(self,
                 query,
                 temporal_query=None,
                 temporal_clause=None,
                 table_name=None,
                 temporal_table_name=None,
                 selected_column=None):
        self.query = query
        self.temporal_query = temporal_query
        self.temporal_clause = temporal_clause
        self.table_name = table_name
        self.temporal_table_name = temporal_table_name
        self.selected_column = selected_column

        self.set_table_names()
        self.set_selected_column()
        self.set_temporal_clause()
        self.build_temporal_query()

    def get_regex_match(query, regex):
        """
        Given a string and regex, return the first match.
        """
        pattern = re.compile(regex)

        matches = pattern.finditer(query)

        for match in matches:
            return str.upper(match.group(0))

    def set_table_names(self):
        TemporalSelectQueryBuilder.set_original_table_name(self)
        TemporalSelectQueryBuilder.set_temporal_table_name(self)

    def set_original_table_name(self):
        original_query = self.query

        match = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=from )[^ ]+')

        self.table_name = str.lower(match)

    def set_temporal_table_name(self):
        self.temporal_table_name = self.table_name + "_history"

    def set_selected_column(self):
        original_query = self.query

        match = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=select )[^ ]+')

        self.selected_column = str.lower(match)

    def set_temporal_clause(self):
        original_query = self.query

        match = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(as of|to|between|contained in)')
        self.temporal_clause = str.lower(match)

    def build_temporal_query(self):
        if self.temporal_clause == "as of":
            TemporalSelectQueryBuilder.as_of_query_builder(self)

        elif self.temporal_clause == "to":
            TemporalSelectQueryBuilder.from_to_query_builder(self)

        elif self.temporal_clause == "between":
            TemporalSelectQueryBuilder.between_and_query_builder(self)

        elif self.temporal_clause == "contained in":
            TemporalSelectQueryBuilder.contained_in_query_builder(self)

        else:
            raise Exception(
                "You entered a wrong temporal keyword or maybe you didn't enter one. Either way, you weren't supposed to see this."
            )

    def as_of_query_builder(self):
        original_query = self.query

        entered_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=as of )[^ ]+')

        column = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=select )[^ ]+')

        self.temporal_query = "select {} from {} where valid_from <= {} and valid_to > {}".format(
            column, self.temporal_table_name, entered_time, entered_time)

    def from_to_query_builder(self):
        original_query = self.query

        start_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query,
            r'(?<={} from )(.*)(?= to)'.format(self.temporal_table_name))

        end_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=to ).*')

        self.temporal_query = "select {} from {} where valid_from < {} and valid_to > {}".format(
            self.selected_column, self.temporal_table_name, end_time,
            start_time)

    def between_and_query_builder(self):
        original_query = self.query

        start_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=between )(.*)(?= and)')

        end_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=and )(.*)')

        self.temporal_query = "select {} from {} where valid_from <= {} and valid_to > {}".format(
            self.selected_column, self.temporal_table_name, end_time,
            start_time)

    def contained_in_query_builder(self):
        original_query = self.query

        start_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=\()(.*)(?=,)')

        end_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=,)(.*)[^\)]+').strip(' ')

        self.temporal_query = "select {} from {} where valid_from >= {} and valid_to <= {}".format(
            self.selected_column, self.temporal_table_name, start_time,
            end_time)
