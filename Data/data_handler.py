import sqlite3
from bin.needed_vars import *
import json as JSON

class sql:

    def __init__(self, lite=True, data_store_location="./Data/sql_data_storage.db", test=False):
        if lite:
            try:
                self.conn = sqlite3.connect(data_store_location)
                self.c = self.conn.cursor()
                self.test = test
            except sqlite3.Error as e:
                log.error("Error connecting to sqlite!\n", e)
                if self.conn:
                    self.conn.close()
    
    def execute(self, sql, values=None, select_one=False, select_all=False, commit=True):
        try:
            log.debug("SQL statement: " + sql)
            if not self.test:
                if values:
                    self.c.execute(sql, values)
                else:
                    self.c.execute(sql)
                if commit:
                    self.conn.commit()
                if select_one:
                    return self.c.fetchone()
                elif select_all:
                    return self.c.fetchall()
        except sqlite3.Error as e:
            log.error("Error executing sql statement: ", sql, "\nError: ", e)
            if self.conn:
                self.conn.close()
    
    def update(self, table, values: dict, condition: tuple):
        sql = f"""UPDATE {table} SET """

        values_conditions = []
        for item, key in values.items():
            if isinstance(key, str):
                values_conditions.append(f"{item}='{key}'")
            else:
                values_conditions.append(f"{item}={key}")
        
        for index, i in enumerate(values_conditions):
            if index != 0:
                i = ', ' + i
            sql += i
        
        if condition:
            if isinstance(condition[1], str):
                sql += f" WHERE {condition[0]}='{condition[1]}'"
            else:
                sql += f" WHERE {condition[0]}={condition[1]}"
        
        self.execute(sql)
    
    def create_table(self, table_name, values: dict):
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("

        for index, key in enumerate(values):
            if index == len(values)-1:
                sql += f"{key} {values[key]})"
            else:
                sql += f"{key} {values[key]}, "
        
        self.execute(sql)
    
    def insert(self, table: str, variables: tuple, values: tuple):
        sql = f"INSERT INTO {table} ("

        for index, i in enumerate(variables):
            if isinstance(i, str):
                i = f"'{i}'"

            if index == len(variables)-1:
                sql += i + ')'
            else:
                sql += i + ', '
        
        sql += " VALUES ("
        for index, _ in enumerate(values):
            if index == len(values)-1:
                sql += '?)'
            else:
                sql += '?, '
        
        self.execute(sql, values=values)
    
    def select(self, table: str, items: str, condition: tuple, select_one=False):
        if condition:
            if isinstance(condition[1], str):
                i = f"'{condition[1]}'"
            else:
                i = condition[1]
            sql = f"SELECT {items} FROM {table} WHERE {condition[0]}={i}"
        else:
            sql = f"SELECT {items} FROM {table}"

        if select_one:
            return self.execute(sql, select_one=True, commit=False)
        else:
            return self.execute(sql, select_all=True, commit=False)

    def delete(self, table: str, condition=tuple):
        sql= f"DELETE FROM {table}"

        if condition:
            value = condition[1]
            if isinstance(value, str):
                value = f"'{value}'"
            
            sql += f" WHERE {condition[0]}={value}"
        
        self.execute(sql)
    
    def drop(self, table: str):
        sql = f"DROP TABLE {table}"
        self.execute(sql)

class json:

    def __init__(self, data_store_location="./Data/json_data.json"):
        self.dsl = data_store_location
        self.data = {}

        self.load_json_data()

    def load_json_data(self):
        try:
            with open(self.dsl, 'r') as f:
                json_data = JSON.load(f)
            self.data = json_data
        except:
            return {}
    
    def add_data(self, key, item):
        self.data[key] = item
        self.write()

    def write(self):
        with open(self.dsl, 'w') as f:
            JSON.dump(self.data, f, indent=4)

    def convert_dict_to_json(self, dictionary):
        return JSON.dumps(dictionary)
    
    def convert_json_to_dict(self, json_data):
        return JSON.loads(json_data)