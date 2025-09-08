from sklearn.base import BaseEstimator, TransformerMixin
import joblib
class EncodeHighCardFeatures(BaseEstimator, TransformerMixin):
  def __init__(self, mapping_dict):
    self.columns = ['emp_title', 'title', 'addr_state']
    self.dict = joblib.load("models/mapping_dict.joblib")

  def fit(self, X, y=None):
    return self
  def transform(self, X):
    X_tf = X.copy()
    for col in self.columns:
      if (col in X_tf.columns) and (col in self.dict):
        X_tf[col] = X_tf[col].map(self.dict[col])
    return X_tf