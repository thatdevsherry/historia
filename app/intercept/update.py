# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import time
import sqlite3


class UpdateQueryBuilder:
    def __init__(self,
                 query,
                 connection,
                 temporal_query=None,
                 temporal_query_insert=None,
                 row_tuple=None,
                 table_name=None,
                 temporal_table_name=None,
                 reference_column_name=None,
                 reference_column_value=None):
        self.query = query
        self.temporal_query = temporal_query
        self.connection = connection
        self.temporal_query_insert = temporal_query_insert
        self.row_tuple = row_tuple
        self.table_name = table_name
        self.temporal_table_name = temporal_table_name
        self.reference_column_name = reference_column_name
        self.reference_column_value = reference_column_value

        self.set_table_names()
        self.build_queries()

    def set_original_table_name(self):
        original_query = self.query.query
        for word in original_query:
            if word == "update":
                table_name_index = original_query.index(word) + 1
                self.table_name = original_query[table_name_index]
                break
            else:
                pass

    def set_temporal_table_name(self):
        table_name = self.table_name
        self.temporal_table_name = table_name + "_history"

    def set_table_names(self):
        UpdateQueryBuilder.set_original_table_name(self)
        UpdateQueryBuilder.set_temporal_table_name(self)

    def build_queries(self):
        UpdateQueryBuilder.build_temporal_query(self)
        UpdateQueryBuilder.build_temporal_query_insert(self)

    def build_temporal_query(self):
        original_query = self.query.query

        for word in original_query:
            if word == "where":
                where_keyword_index = original_query.index(word)
                break
            else:
                pass

        # we assume user entered column_name=value (without spaces) for now

        # TODO: see if user entered column_name=value or without spaces
        # and then parse correctly

        reference_column = original_query[where_keyword_index + 1]
        split_word = reference_column.split('=')
        column_name = split_word[0]
        self.reference_column_name = column_name
        column_value = split_word[1]
        self.reference_column_value = column_value

        # get current date
        day = time.localtime()[2]
        month = time.localtime()[1]
        year = time.localtime()[0]

        date_string = "{}-{}-{}".format(year, month, day)

        temporal_query = "update {} set valid_to='{}' where {}={}".format(
            self.temporal_table_name, date_string, column_name, column_value)

        self.temporal_query = temporal_query

    def build_temporal_query_insert(self):
        original_query = self.query.query
        for word in original_query:
            if word == "set":
                set_keyword_index = original_query.index(word)
            else:
                pass

        change_value_word = original_query[set_keyword_index + 1]
        split_word = change_value_word.split('=')
        column_name = split_word[0]
        new_value = split_word[1].strip("'")

        # get full row
        query = self.connection.execute(
            "select * from {} where {} = {}".format(
                self.table_name, self.reference_column_name,
                self.reference_column_value))
        query_result = query.fetchone()
        self.row_tuple = query_result

        get_name_query = self.connection.execute(
            "select {} from {} where {} = {}".format(
                column_name, self.table_name, self.reference_column_name,
                self.reference_column_value))

        previous_value = get_name_query.fetchone()[0]

        # get current date
        day = time.localtime()[2]
        month = time.localtime()[1]
        year = time.localtime()[0]

        date_string = "{}-{}-{}".format(year, month, day)

        query_result_list = list(query_result)
        old_value_index = query_result_list.index(previous_value)
        query_result_list.pop(old_value_index)
        query_result_list.insert(old_value_index, new_value)
        query_result_list.append(date_string)
        query_result_list.append('')
        new_tuple = tuple(query_result_list)

        insert_query = "insert into {} values {}".format(
            self.temporal_table_name, new_tuple)

        self.temporal_query_insert = insert_query
