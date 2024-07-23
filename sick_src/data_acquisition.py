import threading
import json
import os
import datetime
import time


class DataAcquisition:
  """
  A class for acquiring data from a sensor, extracting features, and writing data to a local file.
  """

  def __init__(self, sensor, sampling_rate, db, data_dir:str="data"):
    self.sensor = sensor #Sensor object
    self.sampling_rate = sampling_rate
    self.data_dir = data_dir
    self.db = db #Database object
    self.running = False
    self.thread = None

    os.makedirs(self.data_dir, exist_ok=True)

  def start_acquisition(self):
    """
    Starts the data acquisition thread.
    """
    if self.running:
      print("Data acquisition already running.")
      return

    self.running = True
    self.thread = threading.Thread(target=self._acquisition_loop)
    self.thread.start()

  def stop_acquisition(self):
    """
    Stops the data acquisition thread.
    """
    if not self.running:
      print("Data acquisition not running.")
      return

    self.running = False
    self.thread.join()  # Wait for the thread to finish

  def _acquisition_loop(self):
    """
    Internal loop that continuously reads data from the sensor, records the time, and writes them to a file and database.
    """
    while self.running:
      data = self.sensor.get_sensor_data()
      timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
      data["timestamp"] = timestamp

      filename = f"{timestamp}.json"
      filepath = os.path.join(self.data_dir, filename)

      self._write_data_to_file(filepath, data)
      self._write_data_to_db(data)
      
      time.sleep(1 / self.sampling_rate)

  def _write_data_to_file(self, filepath, data):
    """
    Writes data to a JSON file.

    Args:
        filepath: The path to the file to write data to.
        data: A dictionary containing sensor data and other features.
    """
    with open(filepath, "w") as f:
      json.dump(data, f, indent=4)

  def _write_data_to_db(self, data):
    """
    Writes data to a database.
    Args:
      data: A dictionary contianing sensor data and other features.
    """
    self.db.create_tables()
    data_id = self.db.insert_raw_data(data)


# if __name__ == "__main__":
#   from database import DBConnection
#   from sensor import Sensor # TODO: why doesn't this work?
#   db = DBConnection()
#   s = Sensor()
#   d = DataAcquisition(s,db = db, sampling_rate= 1)
#   raw_data = {
#         "timestamp_from": time.time(),
#         "timestamp_to": time.time() + 10,
#         "features": {"temperature": 25.5, "pressure": 1010},
#         # Optional flag (consider using a boolean instead of integer)
#         "flag": 0
#     }

#   d._write_data_to_db(raw_data)


  



