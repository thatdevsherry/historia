"""
Copyright (c) 2019 Muhammad Shehriyar Qureshi

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import re
import datetime

from historia.intercept.create import CreateQueryBuilder
from historia.intercept.delete import DeleteQueryBuilder
from historia.intercept.insert import InsertQueryBuilder
from historia.intercept.select import TemporalSelectQueryBuilder
from historia.intercept.update import UpdateQueryBuilder
from historia.intercept.select_handler import SelectQueryHandler
from historia.query_execution.create import CreateQuery
from historia.query_execution.delete import DeleteQuery
from historia.query_execution.insert import InsertQuery
from historia.query_execution.select import NormalSelectQuery, TemporalSelectQuery
from historia.query_execution.update import UpdateQuery


class QueryHandler:
    def action_handler(connection, query):
        keyword_pattern = re.compile(r"(create|insert|update|delete|select)")
        keyword_matches = keyword_pattern.finditer(query)

        for match in keyword_matches:
            keyword_match = match.group(0)

        if keyword_match == "create":
            query_info = CreateQueryBuilder(query)
            CreateQuery.execute(connection, query_info)

        elif keyword_match == "insert":
            time_string = datetime.datetime.now().isoformat()
            query_info = InsertQueryBuilder(query, time_string)
            InsertQuery.execute(connection, query_info)

        elif keyword_match == "update":
            time_string = datetime.datetime.now().isoformat()
            query_info = UpdateQueryBuilder(query, connection, time_string)
            UpdateQuery.execute(connection, query_info)

        elif keyword_match == "delete":
            time_string = datetime.datetime.now().isoformat()
            query_info = DeleteQueryBuilder(query, time_string)
            DeleteQuery.execute(connection, query_info)

        elif keyword_match == "select":
            if SelectQueryHandler.is_temporal_query(query) is True:
                query_info = TemporalSelectQueryBuilder(query)
                return TemporalSelectQuery.execute(connection, query_info)

            else:
                return NormalSelectQuery.execute(connection, query)
