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

def load_model(filepath):
    '''
    Loads Model (file format is joblib)
    '''
    model = load(filepath)
    return model

def save_model(model, filepath):
    '''
    Dumps Model (file format is joblib)
    '''
    joblib.dump(model, filepath)

def train_model(X, y):
    # Trains Model
    model = xgb.XGBClassifier(verbosity=0)
    model.fit(X, y)
    return model
                    
def retrain_model(model, X, y):
    # Retrains Model
    model.partial_fit(X, y)
    return model


def predict_instance(model, instance):
    '''
    Predicts instance with model
    '''
    y_pred = model.predict(pd.DataFrame([instance.values()], columns=instance.keys()))
    return y_pred

def evaluate_on_holdout(model):
    data = pd.read_csv('./data/holdout.csv')
    x_cols = [x for x in data.columns if (x not in ['ID_code', 'target'])]

    X = data[x_cols]
    y = data['target']

    y_pred = model.predict(X)
    y_true = np.array(y)
    score = utils.get_scores(y_true, y_pred)["f1"]

    return score
