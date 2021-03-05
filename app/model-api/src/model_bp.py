"""
Blueprint with Functions and Routing used on the handling of the machine learning 
model. It includes the definition of endpoints for the training of a new model, 
retraining of a existing model and upload of a new model.
"""

from flask import Blueprint, request
import utils
import base64
import joblib
import pandas as pd
import numpy as np
from os import remove

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
               model: base64_string }
    OUTPUT:
    - output: message
              status (successful or not)
    '''
    input_asDict = request.get_json()

    logger.info("Received [Upload Model Request] (0/3) ... ")

    # Sees if model name is available
    try: 
        # Check if Model Name and Model Type are present
        if ("model_name" in input_asDict.keys()):
            model_name = input_asDict["model_name"]
            filepath = "./models/"+model_name+".joblib.dat"
            if utils.file_exists(filepath):
                message = "Model with given name already exists."
                logger.error(message)
                return utils.custom_response_http(message, 400)
        else:
            model_name = "default_model"
    except: 
        message = "Internal Server Error"
        logger.info(message)
        return utils.custom_response_http(message, 500)
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
            return utils.custom_response_http(message, 400)
    except: 
        message = "Internal Server Error"
        logger.error(message)
        return utils.custom_response_http(message, 500)
    logger.info("[Upload Model Request] Model Decoded (2/3) ... ")

    # Validate Model
    try:
        # Validate with Holdout Set
        data = pd.read_csv('./data/holdout.csv')
        x_cols = [x for x in data.columns if (x not in ['ID_code', 'target'])]

        X = data[x_cols]
        y = data['target']

        y_pred = model.predict(X)
        y_true = np.array(y)

        score = utils.get_scores(y_true, y_pred)["f1"]
    except:
        message = "Could not validate model ."
        # remove(filepath)
        logger.error(message)
        return utils.custom_response_http(message, 500)
    logger.info("[Upload Model Request] Model Validated (3/3) .")
    
    message = "Model Uploaded! Score: " + str(score)
    logger.info(str(utils.custom_response_http(message, 200)))
    return utils.custom_response_http(message, 200)

 
@model_bp.route('/train_model', methods=['POST'])
def train_model():
    ''' 
    Receives a JSON with a batch of instances as payload. If a with the given name and type does
    not exist, a new model is created with the given model type and model name.
    If a model with the given name and type already exists:
        - Trains the model (while keeping the previous weights) if retrain is set to 0;
        - Retrains the model from 0 if retrain is set to 1 (or is inexistent).
    
    INPUT:
    - input: {  model_name : string,
                data: encoded b64string,
                retrain: 0 or 1 }

    OUTPUT:
    - output: message
            status (successful or not)
    '''

    input_asDict = request.get_json()

    logger.info("Received [Train Model Request] (0/) ... ")

    if ("model_name" in input_asDict.keys()):
        model_name = input_asDict["model_name"]
    else:
        message = "Model Name is required."
        logger.error(message)
        return utils.custom_response_http(message, 400)
    logger.info("[Train Model Request] Model Name Set: [" + model_name + "] (1/) ... ")

    # Decodes Training Data
    try:
        if ("data" in input_asDict.keys()):
            data_as64 = input_asDict["data"]
            dataraw = base64.b64decode(data_as64)
            data_filepath = "./tmp/tmpcsv.csv"
            with open(data_filepath, 'wb') as fh:
                fh.write(dataraw)
            data = pd.read_csv(data_filepath)
            logger.info(string(data.head()))
            X, y = utils.split_Xy(data)
        else:
            message = "Data does not exist in request."
            logger.error(message)
            return utils.custom_response_http(message, 400)
    except: 
        message = "Internal Server Error"
        logger.error(message)
        return utils.custom_response_http(message, 500)
    logger.info("[Train Model Request] Decoded Dataset. (2/) ... ")

    # Loads/Creates Model
    try:
        filepath = "./models/" + model_name + ".joblib.dat"
        if model_already_exists(filepath):
            if input_asDict["retrain"] == 1:
                with open(filepath, 'rb') as model_file:
                    # Load model
                    model = joblib.load(model_file)
                    model.partial_fit(X, y)
            else:
                message = "Cannot overwrite model. Set retrain = 1 or choose another name."
                logger.error(message)
                return utils.custom_response_http(message, 400)
        else:
            model = xgb.XGBClassifier(n_jobs=-1,
            objective='binary:logistic',
            random_state=42,
            verbosity=0
            )
            model.fit(X, y)
    except: 
        message = "Internal Server Error"
        logger.error(message)
        return utils.custom_response_http(message, 500)

    return utils.custom_response_http("Model Training was successful! ", 200)