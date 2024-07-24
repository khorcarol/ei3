import json


def batch_train(db, model):

    all_data = db.fetch_all()
    annotated_data = all_data[all_data["annotated"] != -1]
    unannotated_data = all_data[all_data["annotated"] == -1]

    x_train = [list(json.loads(j).values())[1:]
               for j in annotated_data["features"].values]
    model.train(x_train)

    # x_test = [list(json.loads(j).values())[1:]
    #           for j in unannotated_data["features"].values]
    # feature_ids = list(unannotated_data["data_id"])

    # for id, x in zip(feature_ids, x_test):
    #     res = model.predict(x)
    #     db.insert_inference(id, "1", res)


def run(db, model, queue):
    while True:
        data_id = queue.get()
        print(f"Inference consumer received data_id: {data_id}")

        # get features
        features = list(db.fetch_features(data_id).values())[1:]

        res = model.predict(features)
        db.insert_inference(data_id, "1", res)
        print(f"data_id: {data_id}      inference result: {res}")

        queue.task_done()  # Indicate completion of processing this data_id
