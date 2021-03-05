"""
Blueprint with Functions and Routing used on the handling of the machine learning 
model. It includes the definition of endpoints for the training of a new model, 
retraining of a existing model and upload of a new model.
"""

from flask import Blueprint, request
import utils
import base64
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

from logger import get_logger
logger = get_logger(__name__)

from config import get_config
config = get_config()
default_model_name = config["default_model_name"]
default_model_type = config["default_model_type"]

model_bp = Blueprint('model_bp', __name__)

@model_bp.route('/upload_model', methods=['POST'])
def upload_model():
    ''' 
    Receives a base64 encoded pickle file to upload a new the model.

    INPUT:
    - input: { model_name : string,
               model_type: string (example: xgboost, lightgbm, etc),
               model: base64_string }
    OUTPUT:
    - output: message
              status (successful or not)
    '''

    input_asDict = request.get_json()
    req, msg = isModelInfoPresent(input_asDict)

    # Check if Model Name and Model Type are present
    if ("model_name" in input_asDict.keys()):
        model_name = input_asDict["model_name"]
    else:
        message = "Model Name is required."
        logger.error(message)
        return utils.customResponseHttp(message, 400)
    if ("model_type" in input_asDict.keys()):
        model_type = input_asDict["model_type"]
    else:
        message = "Model Type is required."
        logger.error(message)
        return utils.customResponseHttp(message, 400)
    
    # Loads Model to be Used
    try:
        model_as64 = input_asDict["model"]
        decoded_message = base64.b64decode(model_as64)
        if model_type == "xgboost":
            filepath = "./models/xgboost/" + model_name + ".pickle.dat"
            if model_already_exists(filepath):
                message = "Model with that name already exists."
                logger.error(message)
                return utils.customResponseHttp(message, 400)
            else: 
                score = save_uploaded_model(decoded_message, filepath)
    except (FileNotFoundError, pickle.UnpicklingError):
        message = "Error Loading Model"
        logger.error(message)
        return utils.customResponseHttp(message, 500)
    except: 
        message = "Internal Error"
        logger.error(message)
        return utils.customResponseHttp(message, 500)
  
    return utils.customResponseHttp("Model Upload was successful! " + 
                                    "Model score on holdout set: " 
                                    + str(score), 200)

# @model_bp.route('/train_model', methods=['POST'])
# def train_model():
#     ''' 
#     Receives a JSON with a batch of instances as payload. If a with the given name and type does
#     not exist, a new model is created with the given model type and model name.
#     If a model with the given name and type already exists:
#         - Trains the model (while keeping the previous weights) if retrain is set to 0;
#         - Retrains the model from 0 if retrain is set to 1 (or is inexistent).
    
#     INPUT:
#     - input: {  model_name : string,
#                 model_type: string (example: xgboost, lightgbm, etc),
#                 retrain: 0 or 1
#                 data_location: base64_string
#     OUTPUT:
#     - output: message
#               status (successful or not)
#     '''

#     input_asDict = request.get_json()

#     if ("model_name" in input_asDict.keys()):
#         model_name = input_asDict["model_name"]
#     else:
#         message = "Model Name is required."
#         logger.error(message)
#         return utils.customResponseHttp(message, 400)
#     if ("model_type" in input_asDict.keys()):
#         model_type = input_asDict["model_type"]
#     else:
#         message = "Model Type is required."
#         logger.error(message)
#         return utils.customResponseHttp(message, 400)
    
#     # Loads Data and Trains Model
#     try:
#         data_raw = input_asDict["data"]
#         data = pd.DataFrame(d=data_raw)
#         if model_type == "xgboost":
#             filepath = "./models/xgboost/" + model_name + ".pickle.dat"
#             if model_already_exists(filepath):
#                 if input_asDict["retrain"] == 0:
#                     model, score = train_model(data)
#                     save_model(model, filepath)
#                     logger.info("Successfully Retrained the Model.")
#                     return utils.customResponseHttp(message, 200)
#                 else:
#                     model = load_model(filepath)
#                     model, score = retrain_model(model, data)
#                     save_model(model, filepath)
#                 return utils.customResponseHttp(message, 200)
#             else: 
#                 model, score = train_model(data)
#                 save_model(model, filepath)
#     except (FileNotFoundError, pickle.UnpicklingError):
#         message = "Error Loading Model"
#         logger.error(message)
#         return utils.customResponseHttp(message, 500)
#     except: 
#         message = "Internal Error"
#         logger.error(message)
#         return utils.customResponseHttp(message, 500)
  
#     return utils.customResponseHttp("Model Training was successful! " + 
#                                     "Model score on holdout set: " 
#                                     + str(score), 200)

def model_already_exists(filepath):
    if Path(filepath).is_file():
        return True
    else:
        return False

def save_uploaded_model(modelb, filepath):
    with open(filepath, 'wb') as model_file:
        model_file.write(modelb)
    with open(filepath, 'rb') as model_file:
        # Load model
        model = pickle.load(model_file)
        # Run model on holdout dataset
        score = evaluate_on_holdout(model)
    return score

def save_model(model, filepath):
    pickle.dump(model, open(filepath, "wb"))

def load_model(filepath):
    with open(filepath, 'rb') as model_file:
        model = pickle.load(model_file)
        return model
    return

def train_model(data):
    # Splits X and y
    X, y = utils.split_Xy()
    # Trains Model
    model.fit(X, y)
    # Evaluate on holdout
    scores = utils.evaluate_on_holdout(model)
    return y_pred
                    
def retrain_model(model, data):
    # Splits X and y
    X, y = utils.split_Xy(data)
    # Retrains Model
    model.partial_fit(X, y)
    # Evaluate on holdout
    score = evaluate_on_holdout(model)
    return model, score

def evaluate_on_holdout(model, metric="f1"):
    # Splits X and y
    X, y = utils.get_holdout_data()
    # Makes Prediction
    y_pred = model.predict(X)
    # Evaluate Multiple Metrics
    scores = utils.get_scores(y, y_pred)
    # Select desired Metric
    return scores[metric]