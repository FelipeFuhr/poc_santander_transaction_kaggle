"""
Flask Application containing the Model API. It predicts and handles a 
machine learning model. The specifics of each functionality are better explained within
each specific functionalities blueprint.
"""

from flask import Flask, request, jsonify, make_response
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np
import pickle
import yaml

from utils import customResponseHttp

from logger import get_logger
logger = get_logger(__name__)

default_model_name = ""
default_model_type = ""

# Loads Configuration File
try: 
    with open("config.yaml", "rb") as yaml_file:
        config = yaml.load(yaml_file, Loader=yaml.FullLoader)
        default_model_name = config["default_model_name"]
        default_model_type = config["default_model_type"]
        logger.info("Successfully loaded configurations.")
except (FileNotFoundError, pickle.UnpicklingError):
    logger.error("Could not load the application config file.")
    exit(1)

# Routing
app = Flask(__name__)

@app.route('/health_check', methods=['GET'])
def health():
    try:
        message = "Health Check was successful"
        logger.info(message)
        return customResponseHttp(message, 200)
    except:
        message = "Health Check was not successful"
        logger.error(message)
        return customResponseHttp(message, 500)

from model_bp import model_bp
app.register_blueprint(model_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)