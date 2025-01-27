from TryLoopclass import TryLoop
from LogOrNotclass import LogOrNot

class EzSQLCore(TryLoop):
    @TryLoop.try_func
    def __init__(self, db_file, db_handler):
        super().__init__(log_mode='terminal', log_file_path='ezsql.log')
        self.db_file = self.db_name = db_file
        self.db_handler = db_handler
        self._dynamic_tables = {}
        
    def __getattr__(self, name):
        """This will dynamically create tables as objects whenever called if they do not already exsist"""
        if name not in self._dynamic_tables:
            self.log_debug(f"Dynamically creating table object '{name}'")
            if self.db_handler == 'sqlite3':
                self._dynamic_tables[name] = EzSQLFunctions(table_name=name, db_handler=self.db_handler, db_file=self.db_file)
            else:
                self._dynamic_tables[name] = EzSQLFunctions(table_name=name, db_handler=self.db_handler, db_file=self.db_file, user=self.user, password=self.password, host=self.host, port=self.port)
        return self._dynamic_tables[name]    
     
class EzSQLiteDB(EzSQLCore):
    @TryLoop.try_func
    def __init__(self, db_file):
        self.db_handler = 'sqlite3'
        self.db_file = db_file
        EzSQLCore.__init__(self, self.db_file, self.db_handler)
        self.log_debug(f"EzSQLiteDB class initialized with {db_file}")

class EzMySQLDB(EzSQLCore):
    @TryLoop.try_func
    def __init__(self, db_file, user, password, host, port):
        db_handler = 'mysql'
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        super().__init__(self, db_file, db_handler)
        self.log_debug(f"EzMySQLDB class initialized with {db_file}")
        
class EzPostgreSQLDB(EzSQLCore):
    @TryLoop.try_func
    def __init__(self, db_file, user, password, host, port):
        db_handler = 'postgresql'
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        super().__init__(self, db_file, db_handler)
        self.log_debug(f"EzPostgreSQLDB class initialized with {db_file}")

class EzSQLFunctions():
    @TryLoop.try_func
    def __init__(self, table_name, db_handler, db_file, user=None, password=None, host=None, port=None):
        self.table_name = table_name
        self.db_file = db_file
        self.user = user
        self.password=password
        self.host=host
        self.port=port
        self.db_handler = db_handler
        self.table_name = table_name
        self.select_all_q = "SELECT * FROM {table}"
        self.select_one_q = "SELECT * FROM {table} WHERE {condition} = ?"
        self.select_column_q = "SELECT {columns} FROM {table}"
        self.select_data_q = "SELECT {columns} FROM {table} WHERE {condition} = ?"
        self.insert_q = "INSERT INTO {table} ({columns}) VALUES ({values})"
        self.update_q = "UPDATE {table} SET {columns} WHERE {condition} = ?"
        self.delete_q = "DELETE FROM {table} WHERE {condition} = ?"
        self.drop_q = "DROP TABLE IF EXISTS{table}"
        self.select_distinct_q = "SELECT DISTINCT {columns} FROM {table}"
        self.createtb_q = "CREATE TABLE IF NOT EXISTS {table} ({columns})"
        self.insert_or_ignore_q = "INSERT OR IGNORE INTO {table} ({condition}) VALUES ({values})"
        self.insert_or_replace_q = "INSERT OR REPLACE INTO {table} ({condition}) VALUES ({values})"
        self.conn = None
        if db_handler == 'sqlite3':
            import sqlite3
            setattr(self, 'conn', sqlite3.connect(self.db_file))
        elif db_handler == 'mysql':
            import mysql.connector 
            setattr(self, 'conn', mysql.connector.connect(database=self.db_file, user=self.user, password=self.password, host=self.host, port=self.port))
        elif db_handler == 'postgresql':
            import psycopg2
            setattr(self, 'conn', psycopg2.connect(database=self.db_file, user=self.user, password=self.password, host=self.host, port=self.port))
        else:
            pass
        self.c = self.conn.cursor()
           
    #@TryLoop.try_func
    def close(self):
        self.conn.close()
        #LogOrNot.log_info(f"Connection to {self.db_file} closed")
    
    #@TryLoop.try_func
    def e(self, method, query, params=None):
        """Executes a SQL query dynamically using the specified method (`execute`, `executemany`, or `executescript`).
        
        :param method: The method to use for execution ('execute', 'executemany', or 'executescript')."""
        if self.db_handler == 'sqlite3':
            import sqlite3
            setattr(self, 'conn', sqlite3.connect(self.db_file))
        elif self.db_handler == 'mysql':
            import mysql.connector 
            setattr(self, 'conn', mysql.connector.connect(database=self.db_file, user=self.user, password=self.password, host=self.host, port=self.port))
        elif self.db_handler == 'postgresql':
            import psycopg2
            setattr(self, 'conn', psycopg2.connect(database=self.db_file, user=self.user, password=self.password, host=self.host, port=self.port))
        else:
            pass
        self.c = self.conn.cursor()
        if method == 'execute'and params:
            self.c.execute(query, params)
        elif method == 'execute':
            self.c.execute(query)
        elif method == 'executemany' and params:
            self.c.executemany(query, params)
        elif method == 'executemany':
            self.c.executemany(query, params)
        elif method == 'executescript':
            self.c.executescript(query)
                        
        #LogOrNot.log_info(f"Query executed successfully with {method}")
        
    @TryLoop.try_func
    def exec(self, query, params=None):
        e = self.e 
        if params is None:
            e('execute', query)
        elif params is not None:
            if isinstance(params, list):
                e('executemany', query, params)
            elif isinstance(params, tuple):
                e('execute', query, params)
            elif isinstance(params, str):
                if self.db_handler == 'sqlite3':
                    e('executescript', query)
                else:
                    LogOrNot.log_error(f"Invalid parameters! It appears you attempted to execute a script. That functionality is ONLY available for SQLite3.The current database handler is {self.db.db_handler} and the query passed was is: {query}")
            else:
                pass
        else:
            LogOrNot.log_error("Invalid parameters")# Continue moving the rest of the functions from SQLiteDB to EzSQLiteBase
        self.conn.commit()
        

    @TryLoop.try_func
    def f_a(self, query, params=None):
        self.e('execute', query, params) if params else self.e('execute', query)
        data = self.c.fetchall()
        if data:
            LogOrNot.log_debug(f"Fetched all data: {data}")
        self.close()
        return data
    
    @TryLoop.try_func
    def f_o(self, query, params=None):
        self.e(query, params) if params else self.e(query)
        data = self.c.fetchone()
        if data:
            LogOrNot.log_debug(f"Fetched data: {data}")
        self.close()
        return data
    
    @TryLoop.try_func           
    def create(self, columns):
        """Create a table and set table_name."""
        columns = columns.replace("-int", "INTEGER").replace("-pk", "PRIMARY KEY").replace("-auto", "AUTOINCREMENT").replace("-txt", "TEXT").replace("-fk", "FOREIGN KEY").replace("-ref", "REFERENCES").replace("-ai", "AUTOINCREMENT")
        self.exec(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({columns})")
        LogOrNot.log_debug(f'Table {self.table_name} created with the following columns and parameters:{columns}')
          
    @TryLoop.try_func
    def fetch_all(self):
        """Fetch all rows from a table."""
        query = self.select_all_q.format(table=self.table_name)
        return self.f_a(query)
    
    @TryLoop.try_func
    def fetch_one(self, condition_column, condition_value):
        """Fetch one row from a table."""
        query = self.select_one_q.format(table=self.table_name, condition=condition_column)
        return self.f_o(query, (condition_value,))
    
    @TryLoop.try_func
    def fetch_column(self, columns):
        """Fetch a column from a table."""
        query = self.select_column_q.format(columns=columns, table=self.table_name)
        return self.f_a(query)
    
    @TryLoop.try_func
    def fetch_data(self, columns, condition_column, condition_value):
        """Fetch data from a table."""
        query = self.select_data_q.format(columns=columns, table=self.table_name, condition=condition_column)
        return self.f_a(query, (condition_value,))
    
    @TryLoop.try_func
    def insert(self, columns, values):
        """Insert data into a table."""
        query = self.insert_q.format(table=self.table_name, columns=columns, values=values)
        self.exec(query)
    
    @TryLoop.try_func
    def update(self, columns, condition):
        """Update data in a table."""
        query = self.update_q.format(table=self.table_name, columns=columns, condition=condition)
        self.exec(query)
        
    @TryLoop.try_func
    def delete(self, condition):
        """Delete data from a table."""
        query = self.delete_q.format(table=self.table_name, condition=condition)
        self.exec(query)
        
    @TryLoop.try_func
    def drop(self):
        """Drop a table."""
        query = self.drop_q.format(table=self.table_name)
        self.exec(query)
        
    @TryLoop.try_func
    def insert_or_ignore(self, columns, values):
        """Insert or ignore data into a table."""
        query = self.insert_or_ignore_q.format(table=self.table_name, condition=columns, values=values)
        self.exec(query)
        
    @TryLoop.try_func
    def insert_or_replace(self, columns, values):
        """Insert or replace data into a table."""
        query = self.insert_or_replace_q.format(table=self.table_name, condition=columns, values=values)
        self.exec(query)
        
    @TryLoop.try_func
    def select_distinct(self, columns):
        """Select distinct data from a table."""
        query = self.select_distinct_q.format(table=self.table_name, columns=columns)
        return self.f_a(query)
       