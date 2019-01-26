# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os

from flask import Flask, jsonify, request
from logging.config import dictConfig
from sklearn.externals import joblib


class ModelNotFoundError(Exception):
    pass



def create_app(test_config=None, dummy_test_model=None):
    """
    Create and configure an instance of the Flask basic application

    :param test_config: Configuration dictionary for tests.
    :param dummy_test_model: Dummy model for tests.
    """

    # Define the logging configuration

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(__name__)

    if test_config is None:
        # Load the model given by the environment variable
        app.logger.info("Getting the machine learning model from the ML_MODEL_PATH " +
                        "environment variable.")

        model_path = os.environ.get("ML_MODEL_PATH", None)
        if model_path is None:
            raise ModelNotFoundError("The environment variable \"ML_MODEL_PATH\" " +
                                     "doesn't exist. Please declare it before " +
                                     "starting this application.")

        # TODO: This should check whether the path is a file or a URL
        app.logger.info("Loading model from path %s" % model_path)  
        model = joblib.load(model_path)
        app.logger.info("Model successfully loaded")
    else:
        # In case the app is being tested, update the configuration accordingly
        # And use the dummy test model
        app.logger.info("Loading app for testing")
        app.config.update(test_config)
        model = dummy_test_model

    @app.route("/")
    def index():
        return jsonify({"message": "Hello, World!"})

    return app
