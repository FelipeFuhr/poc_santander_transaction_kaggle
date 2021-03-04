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

    if ("model_name" in input_asDict.keys()):
        model_name = input_asDict["model_name"]
    else:
        message = "Model Name is not present."
        logger.error(message)
        return utils.customResponseHttp(message, 400)
    if ("model_type" in input_asDict.keys()):
        model_type = input_asDict["model_type"]
    else:
        message = "Model Type is not present."
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
                f1_score = save_xgboost_model(decoded_message, filepath)
    except (FileNotFoundError, pickle.UnpicklingError):
        message = "Error Loading Model"
        logger.error(message)
        return utils.customResponseHttp(message, 500)
    except: 
        message = "Internal Error"
        logger.error(message)
        return utils.customResponseHttp(message, 500)
  
    return utils.customResponseHttp("Model Upload was successful! " + 
                                    "Model F1 score on holdout set: " 
                                    + str(f1_score), 200)

def model_already_exists(filepath):
    if Path(filepath).is_file():
        return True
    else:
        return False

def save_xgboost_model(modelb, filepath):
    with open(filepath, 'wb') as model_file:
        model_file.write(modelb)
    with open(filepath, 'rb') as model_file:
        # Load model
        model = pickle.load(model_file)
        # Run model on holdout dataset
        X, y = utils.get_holdout_data()
        y_pred = model.predict(X)
        logger.info(np.array(y_pred) + np.array(y))
        scores = utils.get_scores(y, y_pred)
    return scores["f1"]
    # return scores["f1"]
    # return 1
# @app.route('/train_model', methods=['POST'])
# def train_model():
#     ''' 
#     Receives a JSON with a batch of instances as payload. Trains a model (if retrain 
#     is set to 0), or retrains the model (if retrain is set to 1). 

#     INPUT:
#     - input: {  model_name: string
#                 data: [{input: {"var_1": value_1, ..., "var_n" : value_n}},
#                        {input: {"var_1": value_1, ..., "var_n" : value_n}},
#                        ...                                                   
#                        {input: {"var_1": value_1, ..., "var_n" : value_n}}] }
#                 retrain: 0 or 1
#     OUTPUT:
#     - output: new model name
#     '''

#     input_asDict = request.get_json()

#     # Loads Model to be Used
#     try: 
#         loaded_model = pickle.load(open(filename, 'rb'))        
#     except (FileNotFoundError, pickle.UnpicklingError):
#         return utils.customResponseHttp("Error Loading Model", "", 500)
#     except: 
#         return utils.customResponseHttp("Internal Error", "", 500)
    
#     # Runs Prediction
#     try:
#         corrected_label = loaded_model.predict(sample)
#     except:
#         return utils.customResponseHttp("Could not make Prediction", "corrected_label", 500)
    
#     return utils.customResponseHttp("Reclassification Success!", corrected_label, 200)


# @app.route('/change_default_model', methods=['POST'])
# def upload_new_model():
#     ''' 
#     Receives a base64 encoded pickle file to upload a new the model

#     INPUT: