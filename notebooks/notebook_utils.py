from sklearn.metrics import recall_score, precision_score, accuracy_score, f1_score, roc_auc_score

def gini_score(y_true, y_pred):
    return 2*roc_auc_score(y_true,y_pred)-1

def get_scores(y_true, y_pred, scores=["accuracy", "gini", "f1", "precision", "recall"]):
    resulting_scores = {}
    scores = set(scores)
    if "accuracy" in scores:
        resulting_scores["accuracy"] = accuracy_score(y_true,y_pred)
    if "gini" in scores:
        resulting_scores["gini"] = gini_score(y_true,y_pred)
    if "f1" in scores:
        resulting_scores["f1"] = f1_score(y_true,y_pred)
    if "precision" in scores:
        resulting_scores["precision"] = precision_score(y_true,y_pred)
    if "recall" in scores:
        resulting_scores["recall"] = recall_score(y_true,y_pred)
    return resulting_scores

def print_scores(scores):
    for key, val in scores.items():
        print(key + " score: " + str(val))