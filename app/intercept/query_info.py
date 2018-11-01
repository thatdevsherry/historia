# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from app.intercept.create import CreateQueryBuilder
from app.intercept.delete import DeleteQueryBuilder
from app.intercept.insert import InsertQueryBuilder
from app.intercept.update import UpdateQueryBuilder
from app.sqlite3.query_execution.create import CreateQuery
from app.sqlite3.query_execution.delete import DeleteQuery
from app.sqlite3.query_execution.insert import InsertQuery
from app.sqlite3.query_execution.update import UpdateQuery


class QueryHandler:
    def action_handler(connection, parsed_query):
        if parsed_query.query[0] == "create":
            query_info = CreateQueryBuilder(parsed_query)
            CreateQuery.execute(connection, query_info)

        elif parsed_query.query[0] == "insert":
            query_info = InsertQueryBuilder(parsed_query)
            InsertQuery.execute(connection, query_info)

        elif parsed_query.query[0] == "update":
            query_info = UpdateQueryBuilder(parsed_query, connection)
            UpdateQuery.execute(connection, query_info)

        elif parsed_query.query[0] == "delete":
            query_info = DeleteQueryBuilder(parsed_query)
            DeleteQuery.execute(connection, query_info)
