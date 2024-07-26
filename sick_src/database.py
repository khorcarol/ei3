import pandas as pd
import json
import time
from typing import Dict, Union, List
import sqlite3


class DBConnection:
    '''
    Class which handles all database interfacing
    '''
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
        flag INTEGER DEFAULT 0,
        annotated INTEGER DEFAULT -1
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

    def insert_raw_data(self, data: Dict[str, Union[List[float], float]]) -> int:
        '''
        Inserts new record of raw data into Raw_data table in database.

        Args:
            data    : dictionary of data label to corresponding data

        Returns:
            Integer primary key of record entered.
        '''

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

    def update_raw_data(self, data_id: int, features: Dict[str, Union[List[float], float]]) -> bool:
        '''
        Updates feature column in Raw_data table in database.

        Args:
            data_id     : primary key of the row in Raw_data table that will be updated
            features    : new features that is going to be updated

        Returns:
            Boolean value of whether the update is successful.
        '''

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

    def fetch_features(self, data_id: int) -> Dict[str, Union[List[float], float]]:
        '''
        Get feature column entry in the Raw_data table based on the data_id.

        Args:
            data_id     : primary key of the row in Raw_data table that will be fetched

        Returns:
            Feature dictionary of features.
        '''

        cursor = self.cursor
        cursor.execute(
            f"SELECT features FROM Raw_data WHERE data_id = {data_id}")
        features_json = cursor.fetchone()[0]
        features = json.loads(features_json)
        return features

    def fetch_last_n_processed_features(self, limit: int) -> List[Dict[str, Union[List[float], float]]]:
        '''
        Get most recent n entries in the Raw_data table.

        Args:
            limit     : number of most recent entries to fetch

        Returns:
            List  of feature dictionaries.
        '''

        cursor = self.cursor
        cursor.execute(f"""
        SELECT features FROM Raw_data WHERE flag = 1 ORDER BY data_id DESC LIMIT {limit}
        """)
        features_json = cursor.fetchall()
        features = [json.loads(tupl[0]) for tupl in features_json]
        return features[::-1] 

    def fetch_all_to_df(self): 
        '''
        Fetch all in Raw_data table and returns a dataframe representation of it.

        Returns:
            Pandas dataframe of the Raw_data table
        '''

        sql_query = pd.read_sql_query(
            """
        SELECT * FROM Raw_data
        """,
            self.conn,
        )
        df = pd.DataFrame(sql_query, columns=["data_id", "timestamp_from",
                                              "timestamp_to",
                                              "features",
                                              "flag",
                                              "annotated"])
        return df

    def set_processed_flag(self, data_id: int):
        '''
        Sets processed flag of row in Raw_data table.

        Args:
            data_id     : Row data_id of row to be operated on.

        '''
        cursor = self.cursor
        cursor.execute(
            f"UPDATE Raw_data SET flag = 1 WHERE data_id = {data_id}")
        self.conn.commit()

    def insert_inference(self, feature_data_id, model_used, result):
        '''
        Inserts new record of inference into Inference table in database.
        
        Args:
            feature_data_id     : the row id in Raw_data table which was used to make this inference
            model_used          : string of model name TODO: change to file name?
            result              : 0, if normal. 1, if anomalous

        Returns:
            Integer primary key of record entered.
        '''

        cursor = self.cursor

        # Assuming data dictionary has keys matching table columns
        cursor.execute("""
                       
      INSERT INTO Inference (feature_data_id, model_used, result_produced)
      VALUES (?, ?, ?);
    """, (feature_data_id, model_used, result))
        self.conn.commit()



