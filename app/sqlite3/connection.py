import sqlite3

from app.parser.query_parser import QueryParser
from app.query_action.select import SelectQuery


class Connection:
    def __init__(self, database_file):
        self.database_file = database_file
        self.verify_file_path()

    def verify_file_path(self):
        # raises sqlite3's exception if file path not valid
        sqlite3.connect(self.database_file)

    def get_database_name(self):
        return self.database_file

    def get_temporal_database_name(self):
        temporal_database = "temporal_" + self.database_file
        return temporal_database

    @staticmethod
    def execute(args):
        parsed_query = QueryParser(args)
        basic_keywords = parsed_query.get_basic_keywords()
        temporal_keywords = parsed_query.get_temporal_keywords()
        SelectQuery.perform_query_action(basic_keywords, temporal_keywords)
        return parsed_query
