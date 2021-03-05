"""
Utility functions for usage on the application.
"""

from flask import jsonify, make_response
from sklearn.metrics import recall_score, precision_score, accuracy_score, f1_score, roc_auc_score
import pandas as pd
from pathlib import Path

def custom_response_http(message: str, httpStatus: int):
    ''' 
    Makes a custom http message with json as payload
    
    INPUT:
    - message: str, 
    - httpStatus: int
    OUTPUT:
    - output: json message
    '''
    out = { "Message" : message }
    return make_response(
        jsonify(out),
        httpStatus)

def gini_score(y_true, y_pred):
    return 2*roc_auc_score(y_true,y_pred)-1

def get_scores(y_true, y_pred, scores=["accuracy", "gini", "f1", "precision", "recall"]):
    """
    Calculates accuracy, gini, g1, precision and/or recall scores.
    """
    resulting_scores = {}
    scores = set(scores)
    if "accuracy" in scores:
        resulting_scores["accuracy"] = accuracy_score(y_true,y_pred)
    if "gini" in scores:
        resulting_scores["gini"] = gini_score(y_true,y_pred)
    if "f1" in scores:
        resulting_scores["f1"] = f1_score(y_true,y_pred)
    if "precision" in scores:
        resulting_scores["precision"] = precision_score(y_true,y_pred)
    if "recall" in scores:
        resulting_scores["recall"] = recall_score(y_true,y_pred)
    return resulting_scores

def print_scores(scores):
    """
    Prints scores calculated on get_scores function
    """
    for key, val in scores.items():
        print(key + " score: " + str(val))

def get_holdout_data():
    """
    Reads holdout data from .csv
    """
    data = pd.read_csv('./data/holdout.csv')
    X, y = split_Xy(data)
    return X, y

def split_Xy(data):
    x_cols = [x for x in data.columns if (x not in ['ID_code', 'target'])]
    X = data[x_cols]
    y = data['target']
    
    return X, y

def file_exists(filepath):
    if Path(filepath).is_file():
        return True
    else:
        return False

def validate_data(data):
    return True