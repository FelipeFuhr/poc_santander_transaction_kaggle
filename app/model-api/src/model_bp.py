"""
Blueprint with Functions and Routing used on the handling of the machine learning 
model. It includes the definition of endpoints for the training of a new model, 
retraining of a existing model and upload of a new model.
"""

from flask import Blueprint, request
import base64
import joblib
import pandas as pd
import numpy as np
from os import remove
import xgboost as xgb

from utils import custom_response_http, batch_response_http,get_scores, file_exists
from model_handler import split_Xy, load_model

from logger import get_logger
logger = get_logger(__name__)

from config import get_config
config = get_config()
default_model_name = config["default_model_name"]

model_bp = Blueprint('model_bp', __name__)

@model_bp.route('/upload_model', methods=['POST'])
def upload_model():
    ''' 
    Receives a base64 encoded joblib file to be saved as a new model.

    INPUT:
    - input: { model_name : string,
               model: base64 encoded joblib file }
    OUTPUT:
    - output: message
              status (successful or not)
    '''
    input_asDict = request.get_json()

    logger.info("Received [Upload Model Request] (0/3) ... ")

    # Sees if model name is available
    try: 
        # Check if Model Name and Model Type are present
        if ("model_name" in input_asDict.keys() and input_asDict["model_name"]):
            model_name = input_asDict["model_name"]
        else:
            model_name = default_model_name
        filepath = "./models/"+model_name+".joblib.dat"
        if file_exists(filepath):
            message = "Model with given name already exists. Choose another name."
            logger.error(message)
            return custom_response_http(message, 400)
    except: 
        message = "Internal Server Error"
        logger.info(message)
        return custom_response_http(message, 500)
    logger.info("[Upload Model Request] Model Name Set: [" + model_name + "] (1/3) ... ")

    # Decodes Model
    try:
        if ("model" in input_asDict.keys()):
            model_as64 = input_asDict["model"]
            logger.info(str(model_as64)[:10])
            decoded_model = base64.b64decode(model_as64)
            with open(filepath, 'wb') as fh:
                fh.write(decoded_model)
                with open(filepath, 'rb') as model_file:
                    # Load model
                    model = joblib.load(model_file)
        else:
            message = "Model does not exist in request."
            logger.error(message)
            return custom_response_http(message, 400)
    except: 
        message = "Internal Server Error"
        logger.error(message)
        return custom_response_http(message, 500)
    logger.info("[Upload Model Request] Model Decoded (2/3) ... ")

    # Validate Model
    try:
        # Validate with holdout Set
        data = pd.read_csv('./data/holdout.csv')
        x_cols = [x for x in data.columns if (x not in ['ID_code', 'target'])]

        X = data[x_cols]
        y = data['target']

        y_pred = model.predict(X)
        y_true = np.array(y)

        score = get_scores(y_true, y_pred)["f1"]
    except:
        message = "Could not validate model ."
        # remove(filepath)
        logger.error(message)
        return custom_response_http(message, 500)
    logger.info("[Upload Model Request] Model Validated (3/3) .")
    
    message = "Model Uploaded! Score: " + str(score)
    logger.info(str(custom_response_http(message, 200)))
    return custom_response_http(message, 200)

 
@model_bp.route('/train_model', methods=['POST'])
def train_model():
    ''' 
    Receives a base64 encoded csv file with a batch of instances as payload. 
    If a file with the given name does not exist, a new model is created with the 
    given model name; otherwise, it returns an error.
    
    INPUT:
    - input: { model_name : string,
               data: base64 encoded csv file }

    OUTPUT:
    - output: message
            status (successful or not)
    '''

    input_asDict = request.get_json()

    logger.info("Received [Train Model Request] (0/3) ... ")

    if ("model_name" in input_asDict.keys() and input_asDict["model_name"]):
        model_name = input_asDict["model_name"]
    else:
        message = "Model Name is required."
        logger.error(message)
        return custom_response_http(message, 400)
    logger.info("[Train Model Request] Model Name Set: [" + model_name + "] (1/3) ... ")

    # Decodes Training Data
    try:
        if ("data" in input_asDict.keys()):
            data_as64 = input_asDict["data"]
            dataraw = base64.b64decode(data_as64)
            data_filepath = "./tmp/tmpcsv.csv"
            with open(data_filepath, 'wb') as fh:
                fh.write(dataraw)
            data = pd.read_csv(data_filepath)
            X, y = split_Xy(data)
        else:
            remove(data_filepath)
            message = "Data does not exist in request."
            logger.error(message)
            return custom_response_http(message, 400)
    except: 
        message = "Internal Server Error"
        logger.error(message)
        return custom_response_http(message, 500)
    
    logger.info("[Train Model Request] Decoded Dataset. (2/3) ... ")

    # Loads/Creates Model
    try:
        filepath = "./models/" + model_name + ".joblib.dat"
        if file_exists(filepath):
            message = "Cannot overwrite model. Choose another name."
            logger.error(message)
            return custom_response_http(message, 400)
        else:
            filepath = "./models/"+default_model_name+".joblib.dat"
            old_model = load_model(filepath)
            model = xgb.XGBClassifier(params=old_model.get_xgb_params())
            model = model.fit(X, y)
            joblib.dump(model, filepath)
    except: 
        remove(data_filepath)
        message = "Internal Server Error"
        logger.error(message)
        return custom_response_http(message, 500)
    logger.info("[Train Model Request] Trained Dataset. (3/3) ... ")

    logger.info(type(custom_response_http("bu", 500)))
    remove(data_filepath)
    return custom_response_http("Model Training was successful! ", 200)