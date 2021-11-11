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


class DeleteQueryBuilder:
    def __init__(
        self,
        query,
        local_time,
        temporal_query=None,
        table_name=None,
        temporal_table_name=None,
    ):
        self.query = query
        self.local_time = local_time
        self.temporal_query = temporal_query
        self.table_name = table_name
        self.temporal_table_name = temporal_table_name

        self.set_table_names()
        self.build_temporal_query(local_time)

    def set_table_names(self):
        DeleteQueryBuilder.set_original_table_name(self)
        DeleteQueryBuilder.set_temporal_table_name(self)

    def set_original_table_name(self):
        original_query = self.query

        table_name_pattern = re.compile(r"(?<=from ).\S+")

        table_name_matches = table_name_pattern.finditer(original_query)

        for match in table_name_matches:
            table_name = match

        self.table_name = table_name.group(0)

    def set_temporal_table_name(self):
        self.temporal_table_name = self.table_name + "_history"

    def build_temporal_query(self, time_string):
        original_query = self.query

        condition = DeleteQueryBuilder.get_where_condition(original_query)

        self.temporal_query = "update {} set valid_to='{}' where {} and valid_to='9999-12-31T00:00:00.000000'".format(
            self.temporal_table_name, time_string, condition
        )

    def get_where_condition(original_query):
        where_condition_pattern = re.compile(r"(?<=where )(.*)")

        where_condition_matches = where_condition_pattern.finditer(original_query)

        for match in where_condition_matches:
            condition_match = match

        value = condition_match.group(0)
        return value
