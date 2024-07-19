from sensor import Sensor
from data_acquisition import DataAcquisition
import time


# Example usage (assuming sensor and feature_extraction modules are implemented)
sensor = Sensor()
sampling_rate = 100
data_dir = "data"  # Adjust data directory if needed

data_acquisition = DataAcquisition(sensor, sampling_rate, data_dir)
data_acquisition.start_acquisition()

