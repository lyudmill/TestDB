
'''
Download odbc driver: https://www.postgresql.org/ftp/odbc/versions/
pip install pytest
pip install pyodbc
'''
import pyodbc

FIELDS_TMPL = ["field1 integer", "field2 text", "field3 char(10)", "field4 cidr"]

#___________________________________
# 1. Check command syntax

def test_crtbl_syntax_ok(dbf, gen):
   table_name=gen.random_correct_name(8)
   dbf.exec_create_table(table_name,FIELDS_TMPL)

def test_crtbl_wrong_syntax1(dbf, gen):
    try:
        dbf.exec_sql(f"create table1 ({FIELDS_TMPL})")
    except pyodbc.Error as ex:
        print(f"\nExpected error occured: \n:{ex}")

def test_crtbl_wrong_syntax2(dbf, gen):
    try:
        dbf.exec_sql(f"create table {gen.random_correct_name(8)} {FIELDS_TMPL}")
    except pyodbc.Error as ex:
        print(f"\nExpected error occured: \n:{ex}")
#-----------------------------------
#Check name
def test_crtbl_wrong_name_dup(dbf, gen):
   table_name=gen.random_correct_name()
   dbf.exec_create_table(table_name,FIELDS_TMPL,False)
   dbf.exec_create_table_negative(table_name,FIELDS_TMPL)
   dbf.exec_sql(f"drop table {table_name}")

def test_crtbl_name_min_col_max(dbf, gen):
   dbf.exec_create_table(gen.random_correct_name(1),gen.random_correct_fields(1500))

def test_crtbl_name_max_col_min(dbf, gen):
   dbf.exec_create_table(gen.random_correct_name(64),gen.random_correct_fields(1))

def test_crtbl_col_types_all(dbf, gen):
    failed = []

    for t in gen.get_fields_type():
        try:
            dbf.exec_create_table(gen.random_correct_name(),gen.random_correct_fields(2, t))
        except pyodbc.Error as ex:
            failed.append(t)
            print(ex)
            continue
    print(failed)
    if len(failed) >0:
        raise Exception(f"Error in the following field types: {failed}")



if __name__ == "__main__":
     import dbfixture as db
#    print(random.randrange(1,2))
#    dbm=db.Dbaccess(conn_string)
#    dbm.connect()
#    dbm.create_table("autotable1", "sdjkfl serial", "txt varchar(50)", "floating numeric")
#    dbm.disconnect()
