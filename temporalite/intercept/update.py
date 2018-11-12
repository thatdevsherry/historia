# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import re
import datetime


class UpdateQueryBuilder:
    def __init__(self,
                 query,
                 connection,
                 local_time,
                 temporal_query=None,
                 temporal_query_insert=None,
                 row_tuple=None,
                 table_name=None,
                 temporal_table_name=None):
        self.query = query
        self.temporal_query = temporal_query
        self.connection = connection
        self.local_time = local_time
        self.temporal_query_insert = temporal_query_insert
        self.row_tuple = row_tuple
        self.table_name = table_name
        self.temporal_table_name = temporal_table_name

        self.set_table_names()
        self.build_queries(local_time)

    def set_table_names(self):
        UpdateQueryBuilder.set_original_table_name(self)
        UpdateQueryBuilder.set_temporal_table_name(self)

    def set_original_table_name(self):
        original_query = self.query

        table_name_pattern = re.compile(r'(?<=update )[^ ]+')

        table_name_matches = table_name_pattern.finditer(original_query)

        for match in table_name_matches:
            table_name_match = match

        self.table_name = table_name_match.group(0)

    def set_temporal_table_name(self):
        table_name = self.table_name
        self.temporal_table_name = table_name + "_history"

    def build_queries(self, time_string):
        UpdateQueryBuilder.build_temporal_query(self, time_string)
        UpdateQueryBuilder.build_temporal_query_insert(self, time_string)

    def build_temporal_query(self, date_string):
        original_query = self.query

        condition = UpdateQueryBuilder.get_where_condition(original_query)

        temporal_query = "update {} set valid_to='{}' where {} and valid_to='9999-12-31T00:00:00.000000'".format(
            self.temporal_table_name, date_string, condition)

        self.temporal_query = temporal_query

    def get_where_condition(original_query):
        condition_pattern = re.compile(r'(?<=where )[^ ]+')

        condition_matches = condition_pattern.finditer(original_query)

        for match in condition_matches:
            condition_match = match

        condition = condition_match.group(0)
        return condition

    def build_temporal_query_insert(self, date_string):
        original_query = self.query

        new_value_string = UpdateQueryBuilder.get_new_values(original_query)

        new_value = UpdateQueryBuilder.get_new_value(new_value_string)

        condition = UpdateQueryBuilder.get_where_condition(original_query)

        update_column = UpdateQueryBuilder.get_update_column(original_query)

        query_result = UpdateQueryBuilder.get_full_row(self, condition)

        previous_value = UpdateQueryBuilder.get_only_column_value(
            self, condition, update_column)

        self.temporal_query_insert = UpdateQueryBuilder.build_query(
            self, query_result, previous_value, new_value, date_string)

    def get_new_values(original_query):
        set_value_pattern = re.compile(r'(?<=set )[^ ]+')

        set_value_match = set_value_pattern.finditer(original_query)

        for match in set_value_match:
            set_value_match = match

        set_value_string = set_value_match.group(0)
        return set_value_string

    def get_new_value(new_value_string):
        new_value_pattern = re.compile(r'(?<==)[^ ]+')

        new_value_matches = new_value_pattern.finditer(new_value_string)

        for match in new_value_matches:
            new_value_match = match

        new_value_unstripped = new_value_match.group(0)
        new_value = new_value_unstripped.strip("'")
        return new_value

    def get_update_column(original_query):
        update_column_pattern = re.compile(r'(?<=set )[^=]+')

        update_column_matches = update_column_pattern.finditer(original_query)

        for match in update_column_matches:
            update_column_match = match

        update_column = update_column_match.group(0)
        return update_column

    def get_full_row(self, condition):
        query = self.connection.execute("select * from {} where {}".format(
            self.table_name, condition))
        query_result = query.fetchone()
        self.row_tuple = query_result
        return query_result

    def get_only_column_value(self, condition, update_column):
        get_column_query = self.connection.execute(
            "select {} from {} where {}".format(update_column, self.table_name,
                                                condition))

        previous_value = get_column_query.fetchone()[0]
        return previous_value

    def build_query(self, query_result, previous_value, new_value,
                    date_string):
        query_result_list = list(query_result)
        old_value_index = query_result_list.index(previous_value)
        query_result_list.pop(old_value_index)
        query_result_list.insert(old_value_index, new_value)
        query_result_list.append('{}'.format(date_string))
        query_result_list.append('9999-12-31T00:00:00.000000')
        new_tuple = tuple(query_result_list)

        insert_query = "insert into {} values {}".format(
            self.temporal_table_name, new_tuple)

        return insert_query

    def get_column_values_list(values_string):
        column_value_pattern = re.compile(r'[^=,]+')
        column_value_matches = column_value_pattern.finditer(values_string)

        values = []

        for match in column_value_matches:
            values.append(match)

        return values

    def create_column_value_dictionary(column_value_list):
        """
        Converts column, value list to dictionary.

        Args:
            A list having odd index as column names and even indexes as their
            values. e.g. name='something' would be ['name','something'].

        Return Values:
            A dictionary with keys as column values and key values as column
            values.
        """
        column_value_dictionary = {}
        try:
            for element in column_value_list:
                if column_value_list.index(element) == 0:
                    column_value_dictionary[column_value_list[
                        column_value_list.index(element)]] = column_value_list[
                            column_value_list.index(element) + 1]
                elif column_value_list.index(element) < 2:
                    column_value_dictionary[column_value_list[
                        column_value_list.index(element) +
                        1]] = column_value_list[
                            column_value_list.index(element) + 2]

                elif column_value_list.index(element) >= 2:
                    column_value_dictionary[column_value_list[
                        column_value_list.index(element) +
                        column_value_list.index(element)]] = column_value_list[
                            column_value_list.index(element) +
                            column_value_list.index(element) + 1]

        except IndexError:
            return column_value_dictionary

    def create_new_query_values(self, column_value_dictionary, full_row):
        full_row_list = list(full_row)

        for column in column_value_dictionary.keys():
            query_result = self.connection.execute(
                "select {} from test where {}".format(
                    column,
                    UpdateQueryBuilder.get_where_condition(self.query)))

            old_value = query_result.fetchone()[0]
            old_value_index = full_row_list.index(old_value)
            full_row_list.pop(old_value_index)
            full_row_list.insert(old_value_index,
                                 column_value_dictionary[column])

        return tuple(full_row_list)
