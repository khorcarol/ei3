import pytest
import os
import tempfile
# Assuming your code is in a module named db_module
from sick_src.database import DBConnection
from datetime import datetime, timedelta
import json
import pandas as pd


@pytest.fixture(scope='module')
def db():
    # Create a temporary file for the database
    db_fd, db_path = tempfile.mkstemp()
    db = DBConnection(db_name=db_path)
    db.create_tables()
    yield db
    # Cleanup: Close the database and delete the file
    db.conn.close()
    os.close(db_fd)
    os.remove(db_path)


def test_insert_raw_data(db: DBConnection):
    data = {
        "timestamp": str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")),
        "feature1": [1.0, 2.0, 3.0],
        "feature2": 5.0,
    }
    sensor_id = 1
    data_id = db.insert_raw_data(sensor_id , data )
    assert isinstance(data_id, int)


def test_fetch_features(db):
    data = {
        "timestamp": str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")),
        "feature1": [1.0, 2.0, 3.0],
        "feature2": 5.0,
    }
    sensor_id = 1
    data_id = db.insert_raw_data(sensor_id, data)
    features = db.fetch_features(data_id)
    assert features == {"feature1": [1.0, 2.0, 3.0], "feature2": 5.0}


def test_update_raw_data(db):
    data = {
        "timestamp": str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")),
        "feature1": [1.0, 2.0, 3.0],
        "feature2": 5.0,
    }
    sensor_id = 1
    data_id = db.insert_raw_data(sensor_id, data)
    new_features = {"feature1": [4.0, 5.0, 6.0], "feature2": 10.0}
    success = db.update_raw_data(data_id, new_features)
    assert success
    updated_features = db.fetch_features(data_id)
    assert updated_features == new_features


def test_fetch_last_n_processed_features(db):
    data1 = {"timestamp": str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), "feature1": [
        1.0], "feature2": 1.0, "flag": 1}
    data2 = {"timestamp": str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), "feature1": [
        2.0], "feature2": 2.0, "flag": 1}
    sensor_id = 1
    data_id = db.insert_raw_data(sensor_id, data1)
    data_id = db.insert_raw_data(sensor_id , data2)
    features = db.fetch_last_n_processed_features(2)
    assert len(features) == 2


def test_fetch_all_to_df(db:DBConnection):

    db.delete_all_raw_data()
    data = {"timestamp": str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), "feature1": [
        1.0], "feature2": 1.0, "flag": 1}
    sensor_id = 1
    data_id = db.insert_raw_data(sensor_id, data)
    df = db.fetch_all_to_df()
    assert len(df) == 1, "DataFrame should have one row"
    assert set(df.columns) == {"data_id", "timestamp_from", "timestamp_to",
                               "features", "flag", "annotated"}, "DataFrame columns mismatch"


def test_set_processed_flag(db):
    data = {"timestamp": str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), "feature1": [
        1.0], "feature2": 1.0, "flag": 0}
    sensor_id = 1
    data_id = db.insert_raw_data(sensor_id, data)
    db.set_processed_flag(data_id)
    assert db.fetch_all_to_df()['flag'].iloc[-1] == 1


def test_insert_inference(db):
    data = {"timestamp": str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), "feature1": [
        1.0], "feature2": 1.0, "flag": 1}
    sensor_id = 1
    data_id = db.insert_raw_data(sensor_id , data )
    db.insert_inference(data_id, "model_name", "normal")
    # You would typically check if the inference was inserted correctly, but without a method to fetch inferences, it's challenging.
    # Adding such a method to the DBConnection class could be useful for more comprehensive testing.
