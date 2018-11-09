from distutils.core import setup

setup(
    name='temporalite',
    version='18.11.9',
    download_url=
    'https://github.com/ShehriyarQureshi/temporalite/archive/18.11.9.tar.gz',
    keywords=[
        'temporal', 'database', 'tables', 'history', 'history-table',
        'temporal-table'
    ],
    description='Implement temporal tables using sqlite3 module',
    long_description="""
    This module uses python's sqlite3 module for implementing temporal tables.
    It allows querying the history table to get information about the state
    of table in the past.
    """,
    url='https://www.github.com/ShehriyarQureshi/temporalite.git',
    author='Shehriyar Qureshi',
    author_email='SShehriyar266@gmail.com',
    license='GPLv3',
    packages=[
        'temporalite', 'temporalite.connection', 'temporalite.intercept',
        'temporalite.query_execution', 'temporalite.tests'
    ],
    zip_safe=False,
)
