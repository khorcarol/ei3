from sick_src import visualise
from sick_src import sensor, data_acquisition, database, feature_processing, inference
from threading import Thread
import time
from model import one_class_svm


sensor_obj = sensor.Sensor(ip_address="cogsihq.dyndns.org:8000")
sampling_rate = 100
data_dir = "data"  # Adjust data directory if needed
db_file = "data/data.db"

db_1 = database.DBConnection(db_file)
data_acquisitio_obj = data_acquisition.DataAcquisition(
    sensor_obj, sampling_rate, db_1, data_dir)
data_acquisitio_obj.start_acquisition()

db_2 = database.DBConnection(db_file)
feature_processing_obj = feature_processing.FeatureProcessor()
feature_processing_thread = Thread(target=feature_processing_obj.run,
                         args=(db_2, data_acquisitio_obj.queue,))
feature_processing_thread.start()

db_3 = database.DBConnection(db_file)
model = one_class_svm.OneClassSVMDetector()
inference.batch_train(db_3, model)
inference_thread = Thread(target=inference.run, args=(
    db_3, model, feature_processing_obj.queue,))
inference_thread.start()


db_4 = database.DBConnection(db_file)
visualise.real_time_spectrogram(db_4)
# visualise.real_time_features(db)
