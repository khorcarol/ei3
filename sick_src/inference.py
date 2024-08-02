import time
import json
import sick_src.database as database
import model.anomaly_detection as anomaly_detection


# TODO:need to list which features to train on
def batch_train(db: database.DBConnection, model: anomaly_detection.AnomalyDetection, feature_keys):
    if feature_keys:
        all_data = db.fetch_all_to_df()
        annotated_data = all_data[all_data["annotated"] != -1]
        unannotated_data = all_data[all_data["annotated"] == -1]

        x_train = []
        for data in annotated_data["features"].values:
            d = (json.loads(data))
            x_train.append([v for k,v in d.items() if k in feature_keys])

        # try:
        model.train(x_train)
        # except Exception as inst:
        #     print(inst.args[0])


def run(db:  database.DBConnection, model: anomaly_detection.AnomalyDetection, queue, model_id, feature_selector_obj):
    while True:
        feature_keys = feature_selector_obj.feature_keys
        
        if feature_keys:
            batch_train(db, model, feature_keys)
            data_id = queue.get()
            print(f"Inference consumer received data_id: {data_id}")

            # get features
            features_dict = db.fetch_features(data_id)
            features = [features_dict[ftu] for ftu in feature_keys]
            
            # try:
            res = model.predict(features)
            db.insert_inference(data_id, model_id, res)
            print(f"data_id: {data_id}      inference result: {res}")
            queue.task_done()  # Indicate completion of processing this data_id
            # except Exception as inst:
            #     print(inst.args[0])

        time.sleep(1)
