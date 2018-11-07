from distutils.core import setup

setup(
    name='temporalite',
    description='Implement temporal tables using sqlite3 module',
    url='https://www.github.com/ShehriyarQureshi/temporalite.git',
    author='Shehriyar Qureshi',
    author_email='SShehriyar266@gmail.com',
    license='GPLv3',
    packages=[
        'temporalite',
        'temporalite.connection',
        'temporalite.constants',
        'temporalite.intercept',
        'temporalite.parser',
        'temporalite.sqlite3',
    ],
    zip_safe=False,
)
