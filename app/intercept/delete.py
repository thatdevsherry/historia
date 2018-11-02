# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import time


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
        original_query = self.query.query

        for word in original_query:
            if word == "from":
                from_keyword_index = original_query.index(word)
                break
            else:
                pass

        table_name = original_query[from_keyword_index + 1]
        self.table_name = table_name

    def set_temporal_table_name(self):
        self.temporal_table_name = self.table_name + "_history"

    def build_temporal_query(self):
        original_query = self.query.query

        for word in original_query:
            if word == "where":
                where_keyword_index = original_query.index(word)
                break
            else:
                pass

        reference_keywords = original_query[where_keyword_index + 1]

        # get current time
        day = time.localtime()[2]
        month = time.localtime()[1]
        year = time.localtime()[0]

        time_string = "{}-{}-{}".format(year, month, day)

        temporal_query = "update {} set valid_to='{}' where {}".format(
            self.temporal_table_name, time_string, reference_keywords)

        self.temporal_query = temporal_query
