# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
from temporalite.connection.connection import Connection


def connect(file_name):
    return Connection(file_name)
