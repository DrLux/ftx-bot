# Import pandas library
import pandas as pd
import sqlite3
from pathlib import Path


class DBOrder():
    def __init__(self, cfg) -> None:
        self.db_path = Path(cfg['db_path'])
        self.connection = sqlite3.connect(str(self.db_path))
        self.cursor = self.connection.cursor()
        self.create_table()

    def tables(self):   
        tables = self.cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;").fetchall()
        return tables

    def create_table(self):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS orders (DATE TEXT, MKT_SRC TEXT, MKT_DST TEXT, PRICE INTEGER, SIZE INTEGER, SIDE TEXT, TYPE TEXT, EXCHANGE_ID TEXT)")

    def get_schema(self):
        df = pd.read_sql_query(f"SELECT * FROM orders", self.connection)
        return list(df.columns)

    def insert_order(self,order):
        market_src,market_dst = order['market'].split("/") 
        params = [ order['createdAt'], market_src, market_dst, order['price'], order['size'], order['side'], order['type'], order['id'] ]

        sqlite_insert_with_param = f"INSERT INTO orders (DATE,MKT_SRC,MKT_DST,PRICE,SIZE,SIDE,TYPE,EXCHANGE_ID) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
        try:
            self.cursor.execute(sqlite_insert_with_param, params)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        
        
    def close(self):
        if self.connection:
            self.connection.close()
            print("The SQLite connection is closed")
    
    def printAll(self):
        print("#######################")
        print(self.get_db())
        print("#######################")

    def get_db(self):
        return pd.read_sql_query(f"SELECT * FROM orders", self.connection)