from operator import methodcaller
import pytest
import sys, os
sys.path.insert(0,os.path.dirname(__file__))
import dbfixture
import generator

conn_string = (
    "DRIVER={PostgreSQL Unicode};"
    "DATABASE=postgres;"
    "UID=postgres;"
    "PWD=password;"
    "SERVER=localhost;"
    "PORT=5432;"
    )

@pytest.fixture(scope='module')
def dbf(request):
    DBfixture=dbfixture.Dbaccess(conn_string)
    DBfixture.connect()
    def fin():
        DBfixture.disconnect()
    request.addfinalizer(fin)
    return DBfixture

@pytest.fixture(scope='module')
def gen(request):
    return generator.SqlGenerator()
