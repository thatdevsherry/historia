import sqlite3

from app.parser.query_parser import QueryParser
from app.intercept.query_info import QueryActionInfo


class Connection:
    def __init__(self, database_file):
        self.database_file = database_file
        self.verify_file_path()

    def verify_file_path(self):
        # raises sqlite3's exception if file path not valid
        sqlite3.connect(self.database_file)

    def execute(self, args):
        parsed_query = QueryParser(args)
        query_info = QueryActionInfo.decide_action(parsed_query)
        # perform sqlite query
        connection = sqlite3.connect(self.database_file)
        connection.execute(' '.join(query_info.query.query))
        # perform temporal query
        connection.execute(query_info.temporal_query)
