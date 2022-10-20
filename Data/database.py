import sqlite3
from sqlite3 import Error

class database(object):
    
    def __init__(self, database_location="./Data/database.db"):
        try:
            conn = sqlite3.connect(database_location)
            self.c = conn.cursor()
            self.conn = conn
        except Error as e:
            print("Error __init__", e)
            if conn:
                conn.close()
    
    def execute_table_sql(self, sql):
        try:
            self.c.execute(sql)
            self.conn.commit()
        except Error as e:
            print(e)
    
    def create_users_db(self):
        sql = """CREATE TABLE IF NOT EXISTS users (
                    id integer PRIMARY KEY,
                    discord_id integer,
                    money integer NOT NULL,
                    items text,
                    effects text,
                    debts text,
                    ownerships text
                );"""
        
        self.execute_table_sql(sql)

    def add_user_to_database(self, user_info):
        sql = """INSERT INTO users (discord_id, money, items, effects, debts, ownerships) VALUES (?,?,?,?,?,?)"""

        self.c.execute(sql, user_info)
        self.conn.commit()
    
    def user_exists_in_database(self, discord_id):
        sql = f"""SELECT * FROM users WHERE discord_id={discord_id}"""

        self.c.execute(sql)
        data_found = self.c.fetchall()
        if data_found != []:
            return data_found
        return False
    

    def create_items_db(self):
        sql = """CREATE TABLE IF NOT EXISTS items (
                    id integer PRIMARY KEY,
                    name text,
                    cost integer,
                    amount_owned integer,
                    player_made integer
                );"""
        
        self.execute_table_sql(sql)


    def add_item_to_database(self, info):
        sql = """INSERT INTO items (name, cost, amount_owned, player_made) VALUES (?,?,?,?)"""

        self.c.execute(sql, info)
        self.conn.commit()
    
    def get_item(self, id):
        sql = f"""SELECT * FROM items WHERE id={id}"""

        self.c.execute(sql)
        data_found = self.c.fetchall()
        if data_found != []:
            return data_found
        return False
    
    def update_item_information(self, id, info):
        sql = f"""UPDATE items SET name='{info[0]}', cost={info[1]}, amount_owned={info[2]}, player_made={info[3]} WHERE id={id}"""
        print(sql)

        self.c.execute(sql)
        self.conn.commit()
