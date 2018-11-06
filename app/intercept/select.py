# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
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

    def set_table_names(self):
        TemporalSelectQueryBuilder.set_original_table_name(self)
        TemporalSelectQueryBuilder.set_temporal_table_name(self)

    def set_selected_column(self):
        original_query = ' '.join(self.query.query)

        selected_column_pattern = re.compile(r'(?<=select )[^ ]+')
        selected_column_matches = selected_column_pattern.finditer(
            original_query)

        for match in selected_column_matches:
            selected_column_match = match

        self.selected_column = selected_column_match.group(0)

    def set_original_table_name(self):
        original_query = ' '.join(self.query.query)

        table_name_pattern = re.compile(r'(?<=from )[^ ]+')

        table_name_matches = table_name_pattern.finditer(original_query)

        for match in table_name_matches:
            table_name_match = match
            break

        self.table_name = table_name_match.group(0)

    def set_temporal_table_name(self):
        self.temporal_table_name = self.table_name + "_history"

    def set_temporal_clause(self):
        original_query = ' '.join(self.query.query)

        # get clause
        clause_pattern = re.compile(r'(as of|to|between|contained in)')

        clause_matches = clause_pattern.finditer(original_query)

        for match in clause_matches:
            temporal_clause_match = match

        self.temporal_clause = temporal_clause_match.group(0)

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
                "You entered a wrong temporal keyword or maybe you didn't \
                enter one. Either way, you weren't supposed to see this.")

    def get_regex_match(query, regex):
        entered_time_pattern = re.compile(regex)

        entered_time_matches = entered_time_pattern.finditer(query)

        for match in entered_time_matches:
            entered_time_match = match

        entered_time = str.upper(entered_time_match.group(0))
        return entered_time

    def as_of_query_builder(self):
        original_query = ' '.join(self.query.query)

        entered_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=as of )[^ ]+')

        column = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=select )[^ ]+')

        self.temporal_query = "select {} from {} where valid_from <= {} and valid_to > {}".format(
            column, self.temporal_table_name, entered_time, entered_time)

    def from_to_query_builder(self):
        original_query = ' '.join(self.query.query)

        start_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<={} from )(.*)(?= to)')

        end_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=to ).*')

        self.temporal_query = "select {} from {} where valid_from < {} and valid_to > {}".format(
            self.selected_column, self.temporal_table_name, end_time,
            start_time)

    def between_and_query_builder(self):
        original_query = ' '.join(self.query.query)

        start_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=between )(.*)(?= and)')

        end_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=and )(.*)')

        self.temporal_query = "select {} from {} where valid_from <= {} and valid_to > {}".format(
            self.selected_column, self.temporal_table_name, end_time,
            start_time)

    def contained_in_query_builder(self):
        original_query = ' '.join(self.query.query)

        start_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=\()(.*)(?=,)')

        end_time = TemporalSelectQueryBuilder.get_regex_match(
            original_query, r'(?<=,)(.*)[^\)]+').strip(' ')

        self.temporal_query = "select {} from {} where valid_from >= {} and valid_to <= {}".format(
            self.selected_column, self.temporal_table_name, start_time,
            end_time)
