from distutils.core import setup

setup(
    name='temporalite',
    version='0.1',
    download_url=
    'https://github.com/ShehriyarQureshi/temporalite/archive/0.1.tar.gz',
    keywords=[
        'temporal', 'database', 'tables', 'history', 'history-table',
        'temporal-table'
    ],
    description='Implement temporal tables using sqlite3 module',
    url='https://www.github.com/ShehriyarQureshi/temporalite.git',
    author='Shehriyar Qureshi',
    author_email='SShehriyar266@gmail.com',
    license='GPLv3',
    packages=[
        'temporalite', 'temporalite.connection', 'temporalite.constants',
        'temporalite.intercept', 'temporalite.parser', 'temporalite.sqlite3'
    ],
    zip_safe=False,
)
