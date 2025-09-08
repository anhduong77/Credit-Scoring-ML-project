from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
from optbinning import OptimalBinning
from feature_engine.encoding import WoEEncoder
class DataFrameWrapper(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns
        self.training_data = None
    def fit(self, X, y=None):
      self.trainning_data = pd.DataFrame(X, columns=self.columns)
      return self
    def transform(self, X): 
      return pd.DataFrame(X, columns=self.columns)

class CatWoeTransformer(BaseEstimator, TransformerMixin):
  """
    attributes: woe_dict, columns
  """
  def __init__(self, columns):
    self.woe_dict_ = {}
    self.columns = columns
    self.woe_encoder = WoEEncoder(
    variables=columns,
    ignore_format=True,
    )
  def fit(self, X, y):

    event_df = X.copy()
    event_df['target'] = y
    cat_iv_dict = []
    self.woe_encoder.fit(X, y)
    for col in self.columns:
      col_df = event_df.groupby(by=col)['target'].agg(['sum', 'count'])
      total_events = col_df['sum'].sum(); total_non_events = (col_df['count'] - col_df['sum']).sum()
      if total_events == 0: total_events = 1
      if total_non_events == 0: total_non_events = 1
      col_df['event'] = col_df['sum'] / total_events
      col_df['non_event'] = (col_df['count'] - col_df['sum']) / total_non_events
      col_df['woe'] = col_df.index
      col_df['woe'] = col_df['woe'].map(self.woe_encoder.encoder_dict_[col])
      col_df['iv'] = (col_df['event'] - col_df['non_event']) * col_df['woe']
      col_df.loc['total'] = col_df.sum()
      self.woe_dict_[col] = col_df
    return self
  def transform(self, X):
    X_tfm = self.woe_encoder.transform(X)
    return X_tfm
  
class WoeTransformer(BaseEstimator, TransformerMixin):
  def __init__ (self):
    self.binning_dict = {}
  def fit(self, X, y=None):
    X_num = X.select_dtypes(include='number')
    X_cat = X.select_dtypes(exclude='number')
    binning_num = [OptimalBinning(name=col, dtype="numerical").fit(X_num[col], y) for col in X_num.columns]
    binning_cat = [OptimalBinning(name=col, dtype="categorical", prebinning_method="cart", monotonic_trend=None).fit(X_cat[col], y) for col in X_cat.columns]
    num_dict = dict(zip(X_num.columns, binning_num))
    cat_dict = dict(zip(X_cat.columns, binning_cat))
    self.binning_dict = num_dict | cat_dict
    return self
  def transform(self, X):
    X_transformed = X.copy()
    for col in X_transformed.columns:
      X_transformed[col] = self.binning_dict[col].transform(X_transformed[col], metric="woe")
    return X_transformed