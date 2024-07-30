import threading
import json
import os
import datetime
import time
import queue
import sick_src.sensor as sensor
import sick_src.database as database
from typing import Optional, List, Dict 


class DataAcquisition:
    """
    A class for acquiring data from a sensor and writing data to a local file and database.
    Producer of queue for downstream feature_processing consumer.
    """

    def __init__(self, sensor: sensor.Sensor, sampling_rate: Optional[int] , db: database.DBConnection, data_dir: str = "data"):
        self.sensor = sensor  # Sensor object
        self.sampling_rate = sampling_rate #TODO
        self.data_dir = data_dir
        self.db = db  # Database object
        self.running = False
        self.thread = None
        self.queue = queue.Queue()

        os.makedirs(self.data_dir, exist_ok=True)

    # def start_acquisition(self):
    #     """
    #     Starts the data acquisition thread.
    #     """
    #     if self.running:
    #         print("Data acquisition already running.")
    #         return

    #     self.running = True
    #     self.thread = threading.Thread(target=self._acquisition_loop)
    #     self.thread.start()

    # def stop_acquisition(self):
    #     """
    #     Stops the data acquisition thread.
    #     """
    #     if not self.running:
    #         print("Data acquisition not running.")
    #         return

    #     self.running = False
    #     self.thread.join()  # Wait for the thread to finish

    def _acquisition_loop(self):
        """
        Internal loop that continuously reads data from the sensor, records the time, and writes them to a file and database.
        """
        while True:
            data = self.sensor.get_sensor_data()
            timestamp = str(
                datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
            data["timestamp"] = timestamp
            sensor_id = self.sensor.sensor_id

            filename = f"s{sensor_id}-{timestamp}.json"
            filepath = os.path.join(self.data_dir, filename)

            self._write_data_to_file(filepath, data)
            self._write_data_to_db(data)

            if self.sampling_rate:
                time.sleep(1 / self.sampling_rate)

    def _write_data_to_file(self, filepath, data):
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    def _write_data_to_db(self, data):
        '''
        Writes data acquired from sensor into Raw_data table of database and puts the 
        data_id of the inserted row into its own finished queue.

        '''
        self.db.create_tables()
        data_id = self.db.insert_raw_data(self.sensor.sensor_id, data= data)

        print(f"DataAcquisiton Producer produced data_id: {data_id}")
        self.queue.put(data_id)
