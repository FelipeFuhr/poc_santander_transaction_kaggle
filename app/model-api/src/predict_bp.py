"""
Blueprint with Functions and Routing used on the prediction of the model. 
It includes the definition of endpoints for the prediction of single and 
multiple instances.
"""

from flask import Blueprint, request

import model_handler
import base64
import data_handler
import pandas as pd
import numpy as np
from os import remove

from utils import custom_response_http, batch_response_http,  file_exists
from data_handler import treat_and_validate_instance_data, treat_and_validate_batch_data, load_json_data
from model_handler import load_model

from logger import get_logger
logger = get_logger(__name__)

from config import get_config
config = get_config()
default_model_name = config["default_model_name"]

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/instance_predict', methods=['POST'])
def instance_predict():
    ''' 
    Receives a JSON with a single instance as payload. Makes prediction with model and 
    returns its classification. If model_name is set, it uses the model given by the name 
    (if it exists); otherwise, it uses the default_model.
    
    INPUT:
     - input: { model_name: string, 
                data: {"var_1": value_1, ..., "var_n" : value_n} }
    OUTPUT:
    - output: message
              status (successful or not)
    '''

    input_asDict = request.get_json()

    logger.info("Received [Predict Instance Request] (0/3) ... ")

    # Loads desired Model
    try: 
        # Check if Model Name and Model Type are present
        if ("model_name" in input_asDict.keys() and input_asDict["model_name"]):
            model_name = input_asDict["model_name"]
        else:
            model_name = default_model_name
        filepath = "./models/"+model_name+".joblib.dat"
        logger.info(filepath)
        if file_exists(filepath):
            model = load_model(filepath)
        else:
            message = "Model " + model_name + " does not exist."
            logger.error(message)
            return batch_response_http(message, [], 400)
    except: 
        message = "Internal Server Error"
        logger.info(message)
        return custom_response_http(message, 500)
    logger.info("[Predict Instance Request] Model [%s] loaded (1/3) ... ", model_name)

    # Loads instance to be classified from json
    try:
        if ("data" in input_asDict.keys()):
            data, ok = load_json_data(input_asDict["data"])
            if ok == False:
                message = "Invalid data. Couldn't parse json."
                logger.error(message)
                return custom_response_http(message, 400)
            
            ok = treat_and_validate_instance_data(data)
            if ok == False:
                message = "Invalid data. Wrong format."
                logger.error(message)
                return custom_response_http(message, 400)
        else:
            message = "Instance does not exist."
            logger.error(message)
            return custom_response_http(message, 400)
    except: 
        message = "Internal Server Error"
        logger.error(message)
        return custom_response_http(message, 500)
    logger.info("[Predict Instance Request] Data loaded (2/3) ... ")

    # Runs Prediction
    try:
        result = model_handler.predict_instance(model, data)
    except:
        message = "Could not make Prediction.",
        logger.error(message)
        return custom_response_http(message, 500)
    logger.info("[Predict Instance Request] Prediction Made (3/3) .")

    return custom_response_http("Classification Success! Target: " + str(result), 200)

@predict_bp.route('/batch_predict', methods=['POST'])
def batch_predict():
    ''' 
    Receives CSV with batch of instances as payload. Makes predictions with the 
    model and returns its classification. If model_name is set, it uses the model
    given by the name (if it exists); otherwise, it uses the default_model.

    INPUT:
    - input: { model_name: string, 
               data: csv
    OUTPUT:
    - output: message
              array with target (labeled 0 or 1)
              status (successful or not)
    '''

    input_asDict = request.get_json()

    logger.info("Received [Predict Instance Request] (0/3) ... ")

    # Loads desired Model
    try: 
        # Check if Model Name and Model Type are present
        if ("model_name" in input_asDict.keys() and input_asDict["model_name"]):
            model_name = input_asDict["model_name"]
        else:
            model_name = default_model_name
        filepath = "./models/"+model_name+".joblib.dat"
        if file_exists(filepath):
            model = load_model(filepath)
        else:
            message = "Model " + model_name + " does not exist."
            logger.error(message)
            return batch_response_http(message, [], 400)
    except: 
        message = "Internal Server Error"
        logger.info(message)
        return batch_response_http(message, [], 500)
    logger.info("[Predict Batch Request] Model [%s] loaded (1/3) ... ", model_name)

    # Decodes Prediction Data
    try:
        if ("data" in input_asDict.keys()):
            data_as64 = input_asDict["data"]
            dataraw = base64.b64decode(data_as64)
            data_filepath = "./tmp/tmpcsv.csv"
            with open(data_filepath, 'wb') as fh:
                fh.write(dataraw)
            data = pd.read_csv(data_filepath)
            data, ok = treat_and_validate_batch_data(data)
            if not ok:
                remove(data_filepath)
                message = "Could not treat/validate data."
                logger.error(message)
                return batch_response_http(message, [], 400)
        else:
            message = "Data does not exist in request."
            logger.error(message)
            return batch_response_http(message, [], 400)
    except: 
        remove(data_filepath)
        message = "Internal Server Error"
        logger.error(message)
        return batch_response_http(message, [], 500)
    logger.info("[Predict Batch Request] Data loaded (2/3) ... ")

    # Predicts Data
    try:
        prediction = model.predict(data).tolist()
    except: 
        remove(data_filepath)
        message = "Internal Server Error"
        logger.error(message)
        return custom_response_http(message, 500)
    logger.info("[Predict Batch Request] Prediction Made (3/3) .")

    return batch_response_http("Classification Success!", prediction, 200)
