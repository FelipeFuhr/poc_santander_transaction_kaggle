"""
Blueprint with Functions and Routing used on the prediction of the model. 
It includes the definition of endpoints for the prediction of single and 
multiple instances.
"""

from flask import Blueprint, request

import utils

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
                data: [{input: {"var_1": value_1, ..., "var_n" : value_n}}] }
    OUTPUT:
    - output: target (label 0 or 1), or -1 (failure)
    '''

    input_asDict = request.get_json()

    # Loads Model to be Used
    try: 
        loaded_model = pickle.load(open(filename, 'rb'))        
    except (FileNotFoundError, pickle.UnpicklingError):
        return utils.customResponseHttp("Error Loading Model", "", 500)
    except: 
        return utils.customResponseHttp("Internal Error", "", 500)
    
    # Runs Prediction
    try:
        corrected_label = loaded_model.predict(sample)
    except:
        return utils.customResponseHttp("Could not make Prediction", "corrected_label", 500)
    
    return utils.customResponseHttp("Reclassification Success!", corrected_label, 200)

@predict_bp.route('/batch_predict', methods=['POST'])
def batch_predict():
    ''' 
    Receives a JSON with a batch of instances as payload. Makes predictions with the model and 
    returns its classification.
    If model_name is set, it uses the model given by the name (if it exists);
    otherwise, we use the default_model

    INPUT:
    - input: { model_name: string, 
               data: [{input: {"var_1": value_1, ..., "var_n" : value_n}},
                      {input: {"var_1": value_1, ..., "var_n" : value_n}},
                       ...                                                   
                      {input: {"var_1": value_1, ..., "var_n" : value_n}}] }
    OUTPUT:
    - output: target (label 0 or 1)
    '''

    input_asDict = request.get_json()

    # Loads Model to be Used
    try: 
        loaded_model = pickle.load(open(filename, 'rb'))        
    except (FileNotFoundError, pickle.UnpicklingError):
        return utils.customResponseHttp("Error Loading Model", "", 500)
    except: 
        return utils.customResponseHttp("Internal Error", "", 500)
    
    # Runs Prediction
    try:
        corrected_label = loaded_model.predict(sample)
    except:
        return utils.customResponseHttp("Could not make Prediction", "corrected_label", 500)
    
    return utils.customResponseHttp("Reclassification Success!", corrected_label, 200)