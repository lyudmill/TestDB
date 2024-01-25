import pyodbc

class Dbaccess:
    def __init__(self, conn_string):
        #todo проверка синтакиса строки
        self.conn_string = conn_string

    def connect(self):
        print(f"Connecting to database with conn string: {self.conn_string}")
        #todo  Удалить пароль из строки
        self.conn = pyodbc.connect(self.conn_string, autocommit=True)
        self.crsr = self.conn.cursor()

    def disconnect(self):
        if self.crsr:
            self.crsr.close()
        if self.conn:
            self.conn.close()

    def exec_sql(self, query = None):
        print(f'\nExecuting query: {query}')
        self.crsr.execute(query)

    def exec_create_table_negative(self, name, fields):
        try:
            f = ",".join(fields)
            print(f)
            query = f"CREATE TABLE {name} ({f})"
            print(f'\nExecuting wrong query: {query}')
            tmp_cur = self.conn.execute(query)
            tmp_cur.close()
            raise Exception("Error: Negative testcase passed successfully")
        except pyodbc.Error as ex:
            print(f'\nExpected error occured: \n:{ex}')


    def exec_create_table(self, name, fields, clear=True):
        f = ",".join(fields)
        query = f"CREATE TABLE {name} ({f})"
        print(f'\nExecuting query: {query}')
        tmp_cur = self.conn.execute(query)
        tmp_cur.close()
 #Checking new table
        self.crsr.execute(f"select * from {name}")
        columns = [(column[0], column[1]) for column in self.crsr.description]
        print(columns)
        if clear:
            self.crsr.execute(f"drop table {name}")
