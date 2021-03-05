"""
Blueprint with Functions and Routing used on the prediction of the model. 
It includes the definition of endpoints for the prediction of single and 
multiple instances.
"""

from flask import Blueprint, request

import model_handler
import data_handler
import pandas as pd

import utils

from logger import get_logger
logger = get_logger(__name__)

predict_bp = Blueprint('predict_bp', __name__)

@predict_bp.route('/instance_predict', methods=['POST'])
def instance_predict():
    ''' 
    Receives a JSON with a single as payload. Makes a prediction with the model and 
    returns its classification.
    If model_name is set, it uses the model given by the name (if it exists);
    otherwise, we use the default_model
    
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
        if ("model_name" in input_asDict.keys()):
            model_name = input_asDict["model_name"]
            filepath = "./models/"+model_name+".joblib.dat"
            if utils.file_exists(filepath):
                model = model_handler.load_model(filepath)
            else:
                message = "Model with given name does not exist."
                logger.error(message)
                return utils.custom_response_http(message, 400)
        else:
            model_name = "default_model"
    except: 
        message = "Internal Server Error"
        logger.info(message)
        return utils.custom_response_http(message, 500)
    logger.info("[Predict Instance Request] Model [%s] loaded (1/3) ... ", model_name)

    # Loads instance to be classified from json
    try:
        if ("data" in input_asDict.keys()):
            data, ok = data_handler.load_json_data(input_asDict["data"])
            if ok == False:
                message = "Invalid data. Couldn't parse json."
                logger.error(message)
                return utils.custom_response_http(message, 400)
            
            ok = data_handler.validate_instance_data(data)
            if ok == False:
                message = "Invalid data. Wrong format."
                logger.error(message)
                return utils.custom_response_http(message, 400)
        else:
            message = "Instance does not exist."
            logger.error(message)
            return utils.custom_response_http(message, 400)
    except: 
        message = "Internal Server Error"
        logger.error(message)
        return utils.custom_response_http(message, 500)
    logger.info("[Predict Instance Request] Data loaded (2/3) ... ")

    # Runs Prediction
    try:
        result = model_handler.predict_instance(model, data)
    except:
        message = "Could not make Prediction.",
        logger.error(message)
        return utils.custom_response_http(message, 500)
    logger.info("Prediction Made (3/3) .")

    return utils.custom_response_http("Classification Success! Target: " + str(result), 200)

# @predict_bp.route('/batch_predict', methods=['POST'])
# def batch_predict():
#     ''' 
#     Receives a JSON with a batch of instances as payload. Makes predictions with the model and 
#     returns its classification.
#     If model_name is set, it uses the model given by the name (if it exists);
#     otherwise, we use the default_model

#     INPUT:
#     - input: { model_name: string, 
#                data: [{input: {"var_1": value_1, ..., "var_n" : value_n}},
#                       {input: {"var_1": value_1, ..., "var_n" : value_n}},
#                        ...                                                   
#                       {input: {"var_1": value_1, ..., "var_n" : value_n}}] }
#     OUTPUT:
#     - output: target (label 0 or 1)
#     '''