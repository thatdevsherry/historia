# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import sqlite3

from temporalite.intercept.query_handler import QueryHandler


class Connection:
    def __init__(self, database_file, sqlite_connection=None):
        self.sqlite_connection = sqlite_connection
        self.database_file = database_file
        self.verify_file_path()

    def verify_file_path(self):
        # raises sqlite3's exception if file path not valid
        self.sqlite_connection = sqlite3.connect(self.database_file)

    def execute(self, args):
        return QueryHandler.action_handler(self.sqlite_connection,
                                           str.lower(args))

    def commit(self):
        self.sqlite_connection.commit()

    def close(self):
        self.sqlite_connection.close()
