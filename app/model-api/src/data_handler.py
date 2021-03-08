"""
File responsible for data handling. It includes etl, split and validate.
"""

import json
import pandas as pd 

from logger import get_logger
logger = get_logger(__name__)

def load_json_data(jsonData):
    """
    Loads/Parse Json data and returns it as dict
    """
    try:
        data = json.loads(jsonData)
        return data, True
    except:
        return "", False

def validate_instance_data(data):
    """
    Validates Single Instance to check if it is in the correct format
    """
    # var_0, ..., var_1
    try:
        desired_keys = set()
        for i in range(0, 200):
            desired_keys.add("var_" + str(i))
        
        # Validate if the keys are the desired keys (and only the desired keys):
        if set(data.keys()) == desired_keys:
            return True
        else:
            return False
    except:
        # Could validate json
        return False

def treat_and_validate_batch_data(data: pd.DataFrame):
    """
    Validates a batch of data to see if it is in the correct format (and get rid of the useless columns,
    if there are any)
    """
    # Treats data by getting only the desired columns
    x_cols = [x for x in data.columns if (x not in ['ID_code', 'target'])]
    X = data[x_cols]
    return X, True

    #     desired_keys = []
    #     for i in range(0, 200):
    #         desired_keys.add("var_" + str(i))

    #     # Validate if the keys are the desired keys (and only the desired keys):
    #     if set(data.columns) == set(desired_keys):
    #         return X, True
    #     else:
    #         return None, False
    # except:
    #     # Could not treat and validate data
    #     return None, False