# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import re
import datetime


class DeleteQueryBuilder:
    def __init__(self,
                 query,
                 local_time,
                 temporal_query=None,
                 table_name=None,
                 temporal_table_name=None):
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

        table_name_pattern = re.compile(r'(?<=from ).\S+')

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
            self.temporal_table_name, time_string, condition)

    def get_where_condition(original_query):
        where_condition_pattern = re.compile(r'(?<=where )(.*)')

        where_condition_matches = where_condition_pattern.finditer(
            original_query)

        for match in where_condition_matches:
            condition_match = match

        value = condition_match.group(0)
        return value
