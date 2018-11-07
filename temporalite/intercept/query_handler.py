# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from .create import CreateQueryBuilder
from .delete import DeleteQueryBuilder
from .insert import InsertQueryBuilder
from .select import TemporalSelectQueryBuilder
from .update import UpdateQueryBuilder
from .select_handler import SelectQueryHandler
from ..sqlite3.query_execution.create import CreateQuery
from ..sqlite3.query_execution.delete import DeleteQuery
from ..sqlite3.query_execution.insert import InsertQuery
from ..sqlite3.query_execution.select import (NormalSelectQuery,
                                              TemporalSelectQuery)
from ..sqlite3.query_execution.update import UpdateQuery


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

        elif parsed_query.query[0] == "select":
            if SelectQueryHandler.is_temporal_query(
                    parsed_query.query) is True:
                query_info = TemporalSelectQueryBuilder(parsed_query)
                return TemporalSelectQuery.execute(connection, query_info)

            else:
                return NormalSelectQuery.execute(connection,
                                                 parsed_query.query)
