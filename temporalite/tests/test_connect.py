# Copyright 2018 Shehriyar Qureshi <SShehriyar266@gmail.com>
import subprocess

from temporalite.connect import connect


def teardown_module():
    subprocess.call(["rm", "test_file"])


def test_connect():
    test_connection = connect('test_file')
    assert test_connection is not None
