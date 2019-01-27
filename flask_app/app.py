# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import numpy as np

from flask import Flask, jsonify, request
from logging.config import dictConfig
from sklearn.externals import joblib


class ModelNotFoundError(Exception):
    pass


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def check_parameters(data):
    """
    Checks the parameters sent are correct. Raise InvalidUsage if not.
    :param data: JSON dictionary with parameters to run the recommendations.
    """
    valid_genders = {"M", "F", "O"}
    valid_occupations = {"administrator", "artist", "doctor", "educator",
                         "engineer", "entertainment", "executive", "healthcare",
                         "homemaker", "lawyer", "librarian", "marketing", "none",
                         "other", "programmer", "retired", "salesman",
                         "scientist", "student", "technician", "writer"}

    if "age" not in data.keys():
        raise InvalidUsage("Missing parameter: 'age'")
    elif not isinstance(data["age"], int):
        raise InvalidUsage("The parameter 'age' must be an integer")
    elif "gender" not in data.keys():
        raise InvalidUsage("Missing parameter: 'gender'")
    elif data['gender'] not in valid_genders:
        raise InvalidUsage("The parameter 'gender' must be one of the following: 'M', 'F', 'O'")
    elif "occupation" not in data.keys():
        raise InvalidUsage("Missing parameter: 'occupation'")
    elif data["occupation"] not in valid_occupations:
        raise InvalidUsage("The parameter 'occupation' must be one of the following: %s" %
                           ", ".join("'%s'" % o for o in sorted(valid_occupations)))
    elif not set(data.keys()).issubset({"age", "gender", "occupation"}):
        raise InvalidUsage("The only valid parameters are: 'age', 'gender', and 'occupation'")

    return data


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

    @app.route("/api/recommend", defaults={"max_recs": 10}, methods=["POST"])
    @app.route("/api/recommend/<max_recs>", methods=["POST"])
    def recommend(max_recs):
        if app.config['TESTING']:
            return jsonify({"recommendations": []})

        data = check_parameters(request.get_json())
        movies = [f.split("=", 1)[1] for f in model.steps[0][1].feature_names_
                  if f.startswith("movie")]
        X = [{**data, **{"movie": movie}} for movie in movies]
        recommendations = model.predict(X)  # Predicts over the whole movie dataset
        recommendations = np.argsort(recommendations)[::-1][:max_recs]

        return jsonify({"recommendations": [movies[i] for i in recommendations]})

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
