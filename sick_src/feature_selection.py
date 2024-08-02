import time
from sick_src.database import DBConnection

class FeatureSelector:
    def __init__(self) -> None:
        self.LIMIT = 9  # only pass this limit will we start to feature select
        self.feature_keys = []

    def feature_select(self, db: DBConnection, sensor_id):
        while True:
            
            entries = db.fetch_last_n_processed_features(sensorid=sensor_id, limit = 100)
            if  len(entries)> self.LIMIT:
                feature_dict = entries[-1]
                self.feature_keys = [ k for k,v in feature_dict.items() if isinstance(v, float)]

            time.sleep(1)
            


