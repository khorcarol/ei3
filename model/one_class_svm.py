

import json
import model.anomaly_detection as anomaly_detection
from sklearn.svm import OneClassSVM #TODO

class OneClassSVMDetector(anomaly_detection.AnomalyDetection):
  """Anomaly detection model using a One-Class SVM."""

  def __init__(self, model_id, kernel = 'rbf', nu = 0.5):
    
    model = OneClassSVM(kernel=kernel, nu=nu)  # Default parameters
    self.trained = None
    super().__init__(model_id, model)
    
  def train(self, training_data):
    '''training_data is a list of features'''
    if len(training_data) == 0:
      raise Exception("No training data provided.")
    self.model.fit(training_data)
    self.trained = True

  def predict(self, features):
    if self.trained is not None:
      prediction = self.model.predict([features])
      return 1 if prediction[0] == -1 else 0
    else:
      raise Exception('Model not yet trained')


