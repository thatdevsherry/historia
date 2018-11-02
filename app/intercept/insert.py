# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import time


class InsertQueryBuilder:
    def __init__(self,
                 query,
                 temporal_query=None,
                 primary_key=None,
                 column_name=None,
                 row=None,
                 old_value=None,
                 new_value=None):
        self.query = query
        self.temporal_query = temporal_query
        self.primary_key = primary_key
        self.column_name = column_name
        self.row = row
        self.old_value = old_value
        self.new_value = new_value

        self.build_temporal_query()
        self.set_attributes()

    def build_temporal_query(self):
        original_query = self.query.query
        for word in original_query:
            if word == "into":
                into_keyword_index = original_query.index(word)
            else:
                pass

        table_name = original_query[into_keyword_index + 1]
        table_name_index = original_query.index(table_name)

        temporal_table = table_name + "_history"
        query_list = list(original_query)
        query_list.pop(table_name_index)
        query_list.insert(table_name_index, temporal_table)

        for word in query_list:
            if ')' in word:
                closing_bracket_word_index = query_list.index(word)
                closing_bracket_word = word

        stripped_query = query_list[:closing_bracket_word_index]
        bracket_index = closing_bracket_word.index(')')
        stripped_word = closing_bracket_word[:bracket_index]

        # get current time
        day = time.localtime()[2]
        month = time.localtime()[1]
        year = time.localtime()[0]

        time_string = "{}-{}-{}".format(year, month, day)

        string_with_values = "{}, '{}', NULL)".format(stripped_word,
                                                      time_string)

        stripped_query.append(string_with_values)

        new_query = ' '.join(stripped_query)

        self.temporal_query = new_query

    def set_attributes(self):
        pass
