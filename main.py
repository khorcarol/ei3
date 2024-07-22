
from sensor import Sensor
from data_acquisition import DataAcquisition
import time


# Example usage (assuming sensor and feature_extraction modules are implemented)
sensor = Sensor(ip_address="cogsihq.dyndns.org:8000")
sampling_rate = 100
data_dir = "data"  # Adjust data directory if needed

data_acquisition = DataAcquisition(sensor, sampling_rate, data_dir)
data_acquisition.start_acquisition()


from visualisation import real_time_features,real_time_spectrogram
# real_time_features('data')
real_time_spectrogram('data')
