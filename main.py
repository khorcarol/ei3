from sick_src import sensor, data_acquisition,database, feature_processing
from threading import Thread
import time


sensor_obj = sensor.Sensor(ip_address="cogsihq.dyndns.org:8000")
sampling_rate = 100
data_dir = "data"  # Adjust data directory if needed
db_file = "data/data.db"
db = database.DBConnection(db_file)

data_acquisitio_obj = data_acquisition.DataAcquisition(sensor_obj, sampling_rate, db, data_dir)
data_acquisitio_obj.start_acquisition()

consumer_thread = Thread(target=feature_processing.run, args=(db, data_acquisitio_obj.queue,))
consumer_thread.start()

# from visualisation import real_time_features,real_time_spectrogram
# # real_time_features('data')
# real_time_spectrogram('data')
