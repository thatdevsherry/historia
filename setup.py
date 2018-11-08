from os import path
from distutils.core import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='temporalite',
    version='0.4',
    download_url=
    'https://github.com/ShehriyarQureshi/temporalite/archive/0.4.tar.gz',
    keywords=[
        'temporal', 'database', 'tables', 'history', 'history-table',
        'temporal-table'
    ],
    description='Implement temporal tables using sqlite3 module',
    long_description=long_description,
    url='https://www.github.com/ShehriyarQureshi/temporalite.git',
    author='Shehriyar Qureshi',
    author_email='SShehriyar266@gmail.com',
    license='GPLv3',
    packages=[
        'temporalite', 'temporalite.connection', 'temporalite.intercept',
        'temporalite.sqlite3'
    ],
    zip_safe=False,
)
