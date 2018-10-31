import sqlite3

from app.parser.query_parser import QueryParser
from app.intercept.query_info import QueryHandler


class Connection:
    def __init__(self, database_file, connection=None):
        self.connection = connection
        self.database_file = database_file
        self.verify_file_path()

    def verify_file_path(self):
        # raises sqlite3's exception if file path not valid
        self.connection = sqlite3.connect(self.database_file)

    def execute(self, args):
        parsed_query = QueryParser(args)
        return QueryHandler.action_handler(self.connection, parsed_query)
