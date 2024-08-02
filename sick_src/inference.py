import json
import sick_src.database as database
import model.anomaly_detection as anomaly_detection


# TODO:need to list which features to train on
def batch_train(db: database.DBConnection, model: anomaly_detection.AnomalyDetection, features):

    all_data = db.fetch_all_to_df()
    annotated_data = all_data[all_data["annotated"] != -1]
    unannotated_data = all_data[all_data["annotated"] == -1]

    x_train = [json.loads(annotated_data["features"])[key] for key in features]

    # try:
    model.train(x_train)
    # except Exception as inst:
    #     print(inst.args[0])


def run(db:  database.DBConnection, model: anomaly_detection.AnomalyDetection, queue, model_id, features):
    while True:
        data_id = queue.get()
        print(f"Inference consumer received data_id: {data_id}")

        # get features
        features_dict = db.fetch_features(data_id)
        features = [features_dict[ftu] for ftu in features]
        print(features)
        
        # try:
        res = model.predict(features)
        db.insert_inference(data_id, model_id, res)
        print(f"data_id: {data_id}      inference result: {res}")
        queue.task_done()  # Indicate completion of processing this data_id
        # except Exception as inst:
        #     print(inst.args[0])
