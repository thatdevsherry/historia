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
from distutils.core import setup

setup(
    name="historia",
    version="19.2.1",
    download_url="https://github.com/ShehriyarQureshi/historia/archive/19.2.1.tar.gz",
    keywords=[
        "temporal",
        "database",
        "tables",
        "history",
        "history-table",
        "temporal-table",
    ],
    description="Support for history tables in SQLite using Python's built-in sqlite3 module",
    long_description="""
    This module uses python's sqlite3 module for implementing temporal tables.
    It allows querying the history table to get information about the state
    of table in the past.
    """,
    url="https://www.github.com/ShehriyarQureshi/historia.git",
    author="Shehriyar Qureshi",
    author_email="thatdevsherry@gmail.com",
    license="MIT",
    packages=[
        "historia",
        "historia.connection",
        "historia.intercept",
        "historia.query_execution",
        "historia.tests",
    ],
    zip_safe=False,
)
