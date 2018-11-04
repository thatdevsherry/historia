# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import re
import datetime

from pudb import set_trace


class DeleteQueryBuilder:
    def __init__(self,
                 query,
                 temporal_query=None,
                 table_name=None,
                 temporal_table_name=None,
                 reference_column_name=None,
                 reference_columnd_value=None):
        self.query = query
        self.temporal_query = temporal_query
        self.table_name = table_name
        self.temporal_table_name = temporal_table_name

        self.set_table_names()
        self.build_temporal_query()

    def set_table_names(self):
        DeleteQueryBuilder.set_original_table_name(self)
        DeleteQueryBuilder.set_temporal_table_name(self)

    def set_original_table_name(self):
        set_trace()
        original_query = ' '.join(self.query.query)

        table_name_pattern = re.compile(r'(?<=from ).\S+')

        table_name_matches = table_name_pattern.finditer(original_query)

        for match in table_name_matches:
            table_name = match

        self.table_name = table_name.group(0)

    def set_temporal_table_name(self):
        self.temporal_table_name = self.table_name + "_history"

    def build_temporal_query(self):
        set_trace()
        original_query = ' '.join(self.query.query)

        where_value_pattern = re.compile(r'(?<=where )(.*)')

        where_value_matches = where_value_pattern.finditer(original_query)

        for match in where_value_matches:
            value_match = match

        value = value_match.group(0)

        time_string = datetime.datetime.now().isoformat()

        self.temporal_query = "update {} set valid_to='{}' where {}".format(
            self.temporal_table_name, time_string, value)
