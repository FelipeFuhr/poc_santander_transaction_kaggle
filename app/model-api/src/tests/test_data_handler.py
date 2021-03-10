from data_handler import treat_and_validate_batch_data, treat_and_validate_instance_data
import pandas as pd

def test_treat_and_validate_batch_data():
    columnsTrue = []
    for i in range(0, 200):
        columnsTrue.append("var_" + str(i))

    pdTrue1 = pd.DataFrame(columns=columnsTrue)
    data, ok = treat_and_validate_batch_data(pdTrue1)
    assert ok == True
    pdTrue2 = pd.DataFrame(columns=columnsTrue + ['ID_code', 'target'])
    data, ok = treat_and_validate_batch_data(pdTrue2)
    assert ok == True

    columnsFalse = columnsTrue + ["willFail"]
    pdFalse = pd.DataFrame(columns=columnsFalse)
    data, ok = treat_and_validate_batch_data(pdFalse)
    assert ok == False

def test_treat_and_validate_instance_data(): 
    instanceTrue = dict()
    for i in range(0, 200):
        instanceTrue["var_" + str(i)] = 1.0
    data, ok = treat_and_validate_instance_data(instanceTrue)
    assert ok == True

    instanceTrue["ID_code"] = 1.0
    instanceTrue["target"] = 1.0
    data, ok = treat_and_validate_instance_data(instanceTrue)
    assert ok == True

    instanceFalse = instanceTrue.copy()
    instanceFalse["willFail"] = 1.0
    data, ok = treat_and_validate_instance_data(instanceFalse)
    assert ok == False