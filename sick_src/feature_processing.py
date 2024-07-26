import queue


class FeatureProcessor:

    def __init__(self):
        self.queue = queue.Queue()

    def run(self, db, queue):
        '''
        Consumer of the DataAcquisition queue. Processes the features, updates database,
        and puts into its own queue for downstream inference consumer.
        '''

        while True:
            data_id = queue.get()
            print(f"Feature Processor Consumer received data_id: {data_id}")

            # get features
            features = db.fetch_features(data_id)

            # process features
            features["spectrum"] = self.filter_spectrum(features["spectrum"])

            # update database
            db.update_raw_data(data_id, features)

            # set processed flag
            db.set_processed_flag(data_id)
            queue.task_done()  # Indicate completion of processing this data_id

            self.queue.put(data_id)

    def filter_spectrum(self, spectrum_data, min=100, max=500):
        return [spectrum_data[i] for i in range(len(spectrum_data)) if i <= max and i >= min]
