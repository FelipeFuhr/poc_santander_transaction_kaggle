"""
File responsible for data handling. It includes etl, split and validate.
"""

import json
import pandas as pd 

def load_json_data(jsonData):
    """
    Loads/Parse Json data and returns it as dict
    """
    try:
        data = json.loads(jsonData)
        return data, True
    except:
        return "", False

def treat_and_validate_instance_data(data: dict) -> bool:
    """
    Validates Single Instance to check if it is in the correct format
    """
    # var_0, ..., var_1
    # x_cols = [x for x in data.keys() if (x not in ['ID_code', 'target'])]
    # treatedDict = {}
    # for col in x_cols:
    #     treatedDict[col] = data[col]
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

def treat_and_validate_batch_data(data: pd.DataFrame) -> (pd.DataFrame, bool):
    """
    Validates a batch of data to see if it is in the correct format (and get rid of the useless columns,
    if there are any)
    """
    # Treats data by getting only the desired columns
    x_cols = [x for x in data.columns if (x not in ['ID_code', 'target'])]
    X = data[x_cols]

    desired_keys = []
    for i in range(0, 200):
        desired_keys.append("var_" + str(i))

    # Validate if the keys are the desired keys (and only the desired keys):
    if set(X.columns) == set(desired_keys):
        return X, True
    else:
        return None, False