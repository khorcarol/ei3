
"""
Feature processing,

Feature ranking

"""


def run(db, queue):
    while True:
        data_id = queue.get()
        print(f"Consumer received data_id: {data_id}") 

        #get features
        features = db.fetch_features(data_id)

        #process features
        features["spectrum"] = filter_spectrum(features["spectrum"])

        #update database
        db.update_raw_data(data_id, features)
        
        #set processed flag
        db.set_processed_flag(data_id)
        queue.task_done()  # Indicate completion of processing this data_id


def filter_spectrum(spectrum_data, min=100, max=200):
    return [spectrum_data[i] for i in range(len(spectrum_data)) if i <= max and i >= min]
