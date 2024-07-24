

import json
class OneClassSVMDetector():
  """Anomaly detection model using a One-Class SVM."""

  def __init__(self):
    super().__init__()
    from sklearn.svm import OneClassSVM
    self.model = OneClassSVM()  # Default parameters

  def train(self, training_data):
    '''training_data is a list of features'''
    self.model.fit(training_data)

  def predict(self, features):
    prediction = self.model.predict([features])
    # Anomaly: -1, Normal: 1 (model decision function)
    return 1 if prediction[0] == -1 else 0


