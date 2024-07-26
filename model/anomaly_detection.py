from abc import ABC, abstractmethod


class AnomalyDetection(ABC):
  """Abstract base class for anomaly detection models."""

  def __init__(self, model_id, model):
    self.model_id = model_id
    self.model = model
    

  @abstractmethod
  def train(self, training_data):
    """
    Trains the anomaly detection model on provided data.

    Args:
        training_data (List): A list of data points used for training.
            
    """
    pass

  @abstractmethod
  def predict(self, features):
    """
    Predicts if anomalous for one datapoint, given its set of features using the trained model.

    Args:
        features (object): List of the feature values used for prediction.

    Returns:
        int: 1 if anomaly detected, 0 otherwise.
    """
    pass

