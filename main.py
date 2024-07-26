from sick_src import visualise
from sick_src import sensor, data_acquisition, database, feature_processing, inference
from threading import Thread
import time
from model import one_class_svm
import json
import os
import sys


import argparse

parser = argparse.ArgumentParser(description='Script so useful.')
parser.add_argument("--config", type=str, default="config.json")
args = parser.parse_args()

opt1_value = args.config


with open(opt1_value, "r") as f:
    config = json.load(f)
    print(config)

sensors = config['sensors']


def sensor_run(sensor_id, sensor_ip, model_id, model_kernel, model_nu):
    sensor_obj = sensor.Sensor(sensor_id, ip_address=sensor_ip)
    data_dir = "data"  # Adjust data directory if needed
    db_file = os.path.join("data", "data.db")

    db_1 = database.DBConnection(db_file)
    db_1.create_tables()
    data_acquisitio_obj = data_acquisition.DataAcquisition(
        sensor=sensor_obj, db=db_1, data_dir=data_dir, sampling_rate=None)
    data_acquisitio_obj.start_acquisition()

    db_2 = database.DBConnection(db_file)
    feature_processing_obj = feature_processing.FeatureProcessor()
    feature_processing_thread = Thread(target=feature_processing_obj.run,
                                       args=(db_2, data_acquisitio_obj.queue,))
    feature_processing_thread.start()

    db_3 = database.DBConnection(db_file)
    model = one_class_svm.OneClassSVMDetector(model_id, model_kernel, model_nu)

    inference.batch_train(db_3, model)
    inference_thread = Thread(target=inference.run, args=(
        db_3, model, feature_processing_obj.queue, model_id))
    inference_thread.start()

    db_4 = database.DBConnection(db_file)
    visualise.real_time_spectrogram(db_4)
    # visualise.real_time_features(db_4)


for i in range(len(sensors)):
    sensor_id = config['sensors'][i]['id']
    sensor_ip = config['sensors'][i]['ip']

    model_param = config['models'][0]['parameters']
    model_kernel = model_param['kernel']
    model_nu = model_param['nu']
    model_id = config['models'][0]['id']

    Thread(target=sensor_run, args=(sensor_id, sensor_ip,
           model_id, model_kernel, model_nu)).start()
