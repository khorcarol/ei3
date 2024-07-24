from sick_src import visualise
from sick_src import sensor, data_acquisition, database, feature_processing, inference
from threading import Thread
import time
from model import one_class_svm


sensor_obj = sensor.Sensor(ip_address="cogsihq.dyndns.org:8000")
sampling_rate = 100
data_dir = "data"  # Adjust data directory if needed
db_file = "data/data.db"
db = database.DBConnection(db_file)

data_acquisitio_obj = data_acquisition.DataAcquisition(
    sensor_obj, sampling_rate, db, data_dir)
data_acquisitio_obj.start_acquisition()

feature_processing_obj = feature_processing.FeatureProcessor()
feature_processing_thread = Thread(target=feature_processing_obj.run,
                         args=(db, data_acquisitio_obj.queue,))
feature_processing_thread.start()


model = one_class_svm.OneClassSVMDetector()
inference.batch_train(db, model)
inference_thread = Thread(target=inference.run, args=(
    db, model, feature_processing_obj.queue,))
inference_thread.start()

# visualise.real_time_features(db)
visualise.real_time_spectrogram(db)
