"""
Flask Application containing the Model API. It predicts and handles a 
machine learning model. The specifics of each functionality are better explained within
each specific functionalities blueprint.
"""

from flask import Flask, request, jsonify, make_response
from sklearn.ensemble import GradientBoostingClassifier
import numpy as np

from utils import custom_response_http

from logger import get_logger
logger = get_logger(__name__)

from config import get_config
config = get_config()

def create_app():
    # Routing
    app = Flask(__name__)
    @app.route('/health_check', methods=['GET'])
    def health_check():
        """
        Simple Health Check to see if application is up
        """
        try:
            message = "Health Check was successful!"
            logger.info(message)
            return custom_response_http(message, 200)
        except:
            message = "Health Check was not successful."
            logger.error(message)
            return custom_response_http(message, 500)
    # Import Flask Blueprints
    from model_bp import model_bp
    app.register_blueprint(model_bp, url_prefix='/')
    from predict_bp import predict_bp
    app.register_blueprint(predict_bp, url_prefix='/')
    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9001)
