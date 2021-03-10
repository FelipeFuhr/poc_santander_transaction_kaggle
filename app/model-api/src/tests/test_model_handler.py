import pandas as pd
from model_handler import split_Xy

def test_split_Xy():
    cols = []
    desired_keys_X = set()
    for i in range(0, 200):
        cols.append("var_" + str(i))
        desired_keys_X.add("var_" + str(i))
    cols.append("target")
    data = pd.DataFrame(columns=cols)
    X, y = split_Xy(data)
    assert set(X.columns) == desired_keys_X