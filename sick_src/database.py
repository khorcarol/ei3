import json
import time
from typing import Dict, Union, List
import sqlite3


class DBConnection:
    instance = None  # global instance of database object

    def __new__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = super().__new__(DBConnection)
            return self.instance
        return self.instance

    def __init__(self, db_name='data/data.db'):
        self.name = db_name
        # connect takes url, dbname, user-id, password
        self.conn = self.connect()
        self.cursor = self.conn.cursor()

    def connect(self):
        try:
            # other threads can use the same connection
            return sqlite3.connect(self.name, check_same_thread=False)
        except sqlite3.Error as e:
            pass

    def create_tables(self):
        """
        Creates the 'Raw_data' and 'Inference' tables in the database if they don't exist.
        """

        cursor = self.cursor
        cursor.execute("""
      CREATE TABLE IF NOT EXISTS Raw_data (
        data_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp_from TIMESTAMP NOT NULL,
        timestamp_to TIMESTAMP NOT NULL,
        features JSONB NOT NULL,
        flag INTEGER DEFAULT 0
      );
    """)
        cursor.execute("""
      CREATE TABLE IF NOT EXISTS Inference (
        inference_id INTEGER PRIMARY KEY AUTOINCREMENT,
        feature_data_id INTEGER REFERENCES Raw_data(data_id) ON DELETE CASCADE,
        model_used TEXT NOT NULL,
        result_produced TEXT NOT NULL,
        annotated_data TEXT DEFAULT NULL,
        inference_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    """)
        self.conn.commit()

    def insert_raw_data(self, data: Dict[str, List]) -> int:

        cursor = self.cursor
        timestamp = data["timestamp"]
        del data["timestamp"]
        # Assuming data dictionary has keys matching table columns
        cursor.execute("""
      INSERT INTO Raw_data (timestamp_from, timestamp_to, features, flag)
      VALUES (?, ?, ?, ?);
    """, (timestamp, timestamp, json.dumps(data), data.get("flag", 0)))
        self.conn.commit()
        data_id = cursor.lastrowid

        return data_id
    
    def update_raw_data(self, data_id: int, features: Dict[str, List]) -> bool:

        cursor = self.cursor
        update_query = f"UPDATE Raw_data SET features = ? WHERE data_id = {data_id}"

        parameters = [json.dumps(features)]

        try:
            cursor.execute(update_query, parameters)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating features: {e}")
            return False


    def fetch_features(self, data_id: int) -> Dict[str, Union[str, float, int]]:
        cursor = self.cursor
        cursor.execute(
            f"SELECT features FROM Raw_data WHERE data_id = {data_id}")
        features_json = cursor.fetchone()[0]
        features = json.loads(features_json)
        return features
    
    def set_processed_flag(self, data_id:int):
        cursor = self.cursor
        cursor.execute(
            f"UPDATE Raw_data SET flag = 1 WHERE data_id = {data_id}")
        self.conn.commit()

    def insert_inference(self):
       return

def main():

    db_file = "data/data.db"
    db = DBConnection(db_file)

    db.create_tables()
    raw_data = {
        "timestamp": time.time(),
        "features": {"temperature": 25.5, "pressure": 1010},
        "flag": 1
    }
    data_id = db.insert_raw_data(raw_data)
    f = db.fetch_features(data_id)
    print(f)


if __name__ == "__main__":
    main()
