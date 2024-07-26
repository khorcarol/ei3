

import json
import model.anomaly_detection as anomaly_detection


class OneClassSVMDetector(anomaly_detection.AnomalyDetection):
  """Anomaly detection model using a One-Class SVM."""

  def __init__(self, model_id, kernel = 'rbf', nu = 0.5):
    from sklearn.svm import OneClassSVM
    model = OneClassSVM(kernel=kernel, nu=nu)  # Default parameters
    super().__init__(model_id, model)
    
  def train(self, training_data):
    '''training_data is a list of features'''
    self.model.fit(training_data)

  def predict(self, features):
    prediction = self.model.predict([features])
    return 1 if prediction[0] == -1 else 0


