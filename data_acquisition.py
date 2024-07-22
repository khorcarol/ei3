import threading
import json
import os
import datetime
import time
from sensor import Sensor



class DataAcquisition:
  """
  A class for acquiring data from a sensor, extracting features, and writing data to a local file.
  """

  def __init__(self, sensor, sampling_rate, data_dir="data"):
    """
    Initializes the data acquisition object.

    Args:
        sensor: A sensor object implementing the `read_data` method.
        sampling_rate: The desired sampling rate in Hz.
        data_dir: The directory to store data files. (default: "data")
    """
    self.sensor = sensor
    self.sampling_rate = sampling_rate
    self.data_dir = data_dir
    self.running = False
    self.thread = None

    # Create the data directory if it doesn't exist
    # Create data directory if needed
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
    Internal loop that continuously reads data from the sensor, extracts features, and writes them to a file.
    """
    while self.running:
      # Read data from the sensor
      data = self.sensor.get_sensor_data()
      # Generate a timestamp for filename
      timestamp = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

      # Create filename with timestamp
      filename = f"{timestamp}.json"
      filepath = os.path.join(self.data_dir, filename)

      # Write data to a JSON file
      self._write_data_to_file(filepath, data)

      # Adjust sleep duration based on desired sampling rate
      time.sleep(1 / self.sampling_rate)

  def _write_data_to_file(self, filepath, data):
    """
    Writes data to a JSON file.

    Args:
        filepath: The path to the file to write data to.
        data: A dictionary containing sensor data and extracted features.
    """
    with open(filepath, "w") as f:
      # Write data with indentation for readability
      json.dump(data, f, indent=4)


