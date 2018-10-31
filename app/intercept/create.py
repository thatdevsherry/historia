# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>


class CreateTableQuery:
    def __init__(self,
                 query,
                 temporal_query=None,
                 table_name=None,
                 temporal_table_name=None):
        self.query = query
        self.temporal_query = temporal_query
        self.table_name = table_name
        self.temporal_table_name = temporal_table_name

        self.build_temporal_query()
        self.set_table_names()

    def set_original_table_name(self):
        original_query = self.query.query
        for word in original_query:
            if word == 'table':
                index_of_table_keyword = original_query.index(word)
            else:
                pass

        self.table_name = original_query[index_of_table_keyword + 1]

    def set_temporal_table_name(self):
        table_name = self.table_name
        self.temporal_table_name = table_name + "_temporal"

    def set_table_names(self):
        CreateTableQuery.set_original_table_name(self)
        CreateTableQuery.set_temporal_table_name(self)

    def build_temporal_query(self):
        original_query = self.query.query
        for word in original_query:
            if ')' in word:
                closing_bracket_word_index = original_query.index(word)
                closing_bracket_word = word
            else:
                pass

        stripped_query = original_query[:closing_bracket_word_index]

        # remove bracket and add columns
        bracket_index = closing_bracket_word.index(')')
        stripped_word = closing_bracket_word[:bracket_index]
        string_with_columns = "{}, valid_from date, valid_to date)".format(
            stripped_word)

        query_to_list = list(stripped_query)
        query_to_list.append(string_with_columns)

        for word in query_to_list:
            if word == "table":
                index_of_word = query_to_list.index(word)
            else:
                pass

        table_name_index = index_of_word + 1
        table_name = query_to_list[table_name_index]
        temporal_table = table_name + "_temporal"
        query_to_list[table_name_index] = temporal_table

        new_query = ' '.join(query_to_list)

        self.temporal_query = new_query
