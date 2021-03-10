"""
File responsible for grouping model related functions. It includes load, train and save.
"""

from joblib import dump, load
import xgboost
import utils
import json
import pandas as pd
import numpy as np
import utils

def load_model(filepath: str):
    '''
    Loads Model (file format is joblib)
    '''
    model = load(filepath)
    return model

def save_model(model, filepath: str):
    '''
    Dumps Model (file format is joblib)
    '''
    joblib.dump(model, filepath)

def predict_instance(model, instance: dict) -> int:
    '''
    Predicts instance with model
    '''
    y_pred = model.predict(pd.DataFrame([instance.values()], columns=instance.keys()))
    return y_pred

def evaluate_on_holdout(model) -> float:
    data = pd.read_csv('./data/holdout.csv')
    x_cols = [x for x in data.columns if (x not in ['ID_code', 'target'])]

    X = data[x_cols]
    y = data['target']

    y_pred = model.predict(X)
    y_true = np.array(y)
    score = utils.get_scores(y_true, y_pred)["f1"]

    return score

def get_holdout_data() -> (pd.DataFrame, pd.DataFrame):
    """
    Reads holdout data from .csv
    """
    data = pd.read_csv('./data/holdout.csv')
    X, y = split_Xy(data)
    return X, y

def split_Xy(data: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    """
    Splits data
    """
    x_cols = [x for x in data.columns if (x not in ['ID_code', 'target'])]
    X = data[x_cols]
    y = data['target']
    return X, y

    