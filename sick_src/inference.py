import json
import sick_src.database as database
import model.anomaly_detection as anomaly_detection


def batch_train(db: database.DBConnection, model: anomaly_detection.AnomalyDetection):

    all_data = db.fetch_all_to_df()
    annotated_data = all_data[all_data["annotated"] != -1]
    unannotated_data = all_data[all_data["annotated"] == -1]

    x_train = [list(json.loads(j).values())[1:]
               for j in annotated_data["features"].values]
    try:
        model.train(x_train)
    except Exception as inst:
        print(inst.args[0])


def run(db:  database.DBConnection, model: anomaly_detection.AnomalyDetection, queue, model_id):
    while True:
        data_id = queue.get()
        print(f"Inference consumer received data_id: {data_id}")

        # get features
        features = list(db.fetch_features(data_id).values())[1:]
        try:
            res = model.predict(features)
            db.insert_inference(data_id, model_id, res)
            print(f"data_id: {data_id}      inference result: {res}")
            queue.task_done()  # Indicate completion of processing this data_id
        except Exception as inst:
            print(inst.args[0])
        

        
