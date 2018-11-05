# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import re
import datetime


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
        original_query = ' '.join(self.query.query)

        table_name_pattern = re.compile(r'(?<=update )[^ ]+')

        table_name_matches = table_name_pattern.finditer(original_query)

        for match in table_name_matches:
            table_name_match = match

        self.table_name = table_name_match.group(0)

    def set_temporal_table_name(self):
        table_name = self.table_name
        self.temporal_table_name = table_name + "_history"

    def set_table_names(self):
        UpdateQueryBuilder.set_original_table_name(self)
        UpdateQueryBuilder.set_temporal_table_name(self)

    def build_queries(self):
        date_string = datetime.datetime.now().isoformat()
        UpdateQueryBuilder.build_temporal_query(self, date_string)
        UpdateQueryBuilder.build_temporal_query_insert(self, date_string)

    def build_temporal_query(self, date_string):
        original_query = ' '.join(self.query.query)

        condition_pattern = re.compile(r'(?<=where )[^ ]+')

        condition_matches = condition_pattern.finditer(original_query)

        for match in condition_matches:
            condition_match = match

        condition = condition_match.group(0)

        temporal_query = "update {} set valid_to='{}' where {} and valid_to='9999-12-31T00:00:00.000000'".format(
            self.temporal_table_name, date_string, condition)

        self.temporal_query = temporal_query

    def build_temporal_query_insert(self, date_string):
        original_query = ' '.join(self.query.query)

        set_value_pattern = re.compile(r'(?<=set )[^ ]+')

        set_value_match = set_value_pattern.finditer(original_query)

        for match in set_value_match:
            set_value_match = match

        set_value_string = set_value_match.group(0)

        new_value_pattern = re.compile(r'(?<==)[^ ]+')

        new_value_matches = new_value_pattern.finditer(set_value_string)

        for match in new_value_matches:
            new_value_match = match

        new_value_unstripped = new_value_match.group(0)
        new_value = new_value_unstripped.strip("'")

        where_clause_value_pattern = re.compile(r'(?<=where )[^ ]+')

        where_clause_value_matches = where_clause_value_pattern.finditer(
            original_query)

        for match in where_clause_value_matches:
            where_clause_value_match = match

        where_clause_value = where_clause_value_match.group(0)

        update_column_pattern = re.compile(r'(?<=set )[^=]+')

        update_column_matches = update_column_pattern.finditer(original_query)

        for match in update_column_matches:
            update_column_match = match

        update_column = update_column_match.group(0)

        # get full row
        query = self.connection.execute("select * from {} where {}".format(
            self.table_name, where_clause_value))
        query_result = query.fetchone()
        self.row_tuple = query_result

        get_column_query = self.connection.execute(
            "select {} from {} where {}".format(update_column, self.table_name,
                                                where_clause_value))

        previous_value = get_column_query.fetchone()[0]

        query_result_list = list(query_result)
        old_value_index = query_result_list.index(previous_value)
        query_result_list.pop(old_value_index)
        query_result_list.insert(old_value_index, new_value)
        query_result_list.append('{}'.format(date_string))
        query_result_list.append('9999-12-31T00:00:00.000000')
        new_tuple = tuple(query_result_list)

        insert_query = "insert into {} values {}".format(
            self.temporal_table_name, new_tuple)

        self.temporal_query_insert = insert_query
