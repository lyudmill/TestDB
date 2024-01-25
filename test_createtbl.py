
'''
Download odbc driver: https://www.postgresql.org/ftp/odbc/versions/
pip install pytest
pip install pyodbc
'''
import string

import pyodbc

FIELDS_TMPL = ["field1 integer", "field2 text", "field3 char(10)", "field4 cidr"]

#___________________________________
# 1. Check command syntax

def test_crtbl_syntax_ok(dbf, gen):
    #Simple correct command
    dbf.exec_create_table("simple_table",FIELDS_TMPL)

def test_crtbl_wrong_syntax1(dbf, gen):
    #Wrong sytax for 'table' statement
    dbf.exec_sql_negative(f"create table1 ({FIELDS_TMPL})")

def test_crtbl_wrong_syntax2(dbf, gen):
    #Empty table name
    dbf.exec_sql_negative(f"create table ({FIELDS_TMPL})")

def test_crtbl_wrong_syntax3(dbf, gen):
    #Missing parenthesis
    dbf.exec_sql_negative(f"create table B1 {FIELDS_TMPL}")

def test_crtbl_wrong_syntax4(dbf, gen):
    #Wrong parenthesis
    dbf.exec_sql_negative(f"create table B1 [{FIELDS_TMPL}]")

def test_crtbl_wrong_syntax_nocols(dbf, gen):
    #Empty columns list
    dbf.exec_sql("create table A1 ()")
    dbf.exec_sql("drop table A1")
#-----------------------------------
#Check name
def test_crtbl_wrong_name_dup(dbf, gen):
    #Duplicated table name
    table_name=gen.random_correct_name()
    dbf.exec_create_table(table_name,FIELDS_TMPL,False)
    dbf.exec_create_table_negative(table_name,FIELDS_TMPL)
    dbf.exec_sql(f"drop table {table_name}")

def test_crtbl_wrong_name_lenmore(dbf, gen):
    #Long table name lennth >64 (will be truncated to 64)
    table_name=gen.random_correct_name(64)+"1234"
    dbf.exec_create_table(table_name,FIELDS_TMPL)

def test_crtbl_wrong_name_null(dbf, gen):
    #Empty name
    dbf.exec_create_table_negative("",FIELDS_TMPL)

def test_crtbl_wrong_name_punctuation(dbf, gen):
    #Cheking all special symbols
    failed = []
    for s in gen.get_special_symbols():
        print(f"\nChecking symbol {s} in table name")
        if s=="$":
            continue
        try:
            dbf.exec_create_table_negative(gen.random_wrong_name(wsymbol=s),FIELDS_TMPL)
        except pyodbc.Error as ex:
            failed.append(s)
            print(ex)
            continue
    if len(failed) >0:
        raise Exception(f"Error in the following symbols: {failed}")
def test_crtbl_name_col_with_parenthesis(dbf, gen):
    #Cheking all special symbols in table and column name
    #%!"#$%&'()*+,-./:;<=>?@[\]^`{|~
    spec_name = gen.get_special_symbols()
    print(f"\nSpecial symbols {spec_name}")
    dbf.exec_create_table(f"\"{spec_name}\"", [f"\"{spec_name}1\" integer", f"\"2{spec_name}\" text", f"\"{spec_name}3\" money"])

def test_crtbl_name_min_col_max(dbf, gen):
    #Name length =1(min) and columns number = 1600 (max)
    table_name = gen.random_correct_name(1)
    dbf.exec_create_table(table_name,gen.random_correct_fields(1600),False)
    cols = len(dbf.crsr.description)
    dbf.exec_sql(f"drop table {table_name}")
    print(f"Column number is {cols}")
    if not cols == 1600:
       raise Exception("Columns number differs from expected")

def test_crtbl_name_max_col_min(dbf, gen):
    #Name length =1(min) and columns number = 1600 (max)
    table_name = gen.random_correct_name(64)
    dbf.exec_create_table(table_name,gen.random_correct_fields(1),False)
    cols = len(dbf.crsr.description)
    dbf.exec_sql(f"drop table {table_name}")
    print(f"Column number is {cols}")
    if not cols == 1:
       raise Exception("Columns number differs from expected")

#Check columns
def test_crtbl_col_types_all(dbf, gen):
    #check all types except 'serial' (separate test for 'serial')
    failed = []
    for t in gen.get_fields_type():
        try:
            dbf.exec_create_table(gen.random_correct_name(),gen.random_correct_fields(2, t))
        except pyodbc.Error as ex:
            failed.append(t)
            print(ex)
            continue

#try lowercase types
    for t in gen.get_fields_type():
        try:
            dbf.exec_create_table(gen.random_correct_name(),gen.random_correct_fields(2, t))
        except pyodbc.Error as ex:
            failed.append(t.lower())
            print(ex)
            continue

#try uppercase types
    for t in gen.get_fields_type():
        try:
            dbf.exec_create_table(gen.random_correct_name(),gen.random_correct_fields(2, t.upper()))
        except pyodbc.Error as ex:
            failed.append(t.upper())
            print(ex)
            continue

    if len(failed) >0:
        raise Exception(f"Error in the following field types: {failed}")

def test_crtbl_wrong_col_type(dbf, gen):
    #Not existing column type
    dbf.exec_create_table_negative(gen.random_correct_name(5),"a1 notexist, b1 integer")

def test_crtbl_wrong_col_more(dbf, gen):
    #Column numbers more than 1600
    dbf.exec_create_table_negative(gen.random_correct_name(),gen.random_correct_fields(1601))

def test_crtbl_wrong_col_serial(dbf, gen):
    #Test for type 'serial', not first
    dbf.exec_create_table_negative(gen.random_correct_name(5),"a1 integer, b1 serial, c1 serial")

def test_crtbl_col_serial(dbf, gen):
    #Test for 'serial' at the fist place
    dbf.exec_create_table(gen.random_correct_name(5),["a1 serial"]+gen.random_correct_fields(10))

def test_crtbl_col_number(dbf, gen):
    #Different admited number of columns
    numbers = (10,500,999,1024,1303,1400,1505,1599)
    failed = []
    for colnum in numbers:
        table_name = gen.random_correct_name()
        dbf.exec_create_table(table_name,gen.random_correct_fields(colnum),False)
        cols = len(dbf.crsr.description)
        dbf.exec_sql(f"drop table {table_name}")
        print(f"Column number is {cols}")
        if not cols == colnum:
            failed.append(f"Error: Columns number is {cols}, expected {colnum}")

    if len(failed):
        print(failed)
        raise Exception("Columns number differs from expected")


if __name__ == "__main__":
     import dbfixture as db
#    print(random.randrange(1,2))
#    dbm=db.Dbaccess(conn_string)
#    dbm.connect()
#    dbm.create_table("autotable1", "sdjkfl serial", "txt varchar(50)", "floating numeric")
#    dbm.disconnect()
