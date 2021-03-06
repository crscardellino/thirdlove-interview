# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import os
import numpy as np
import uuid

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from logging.config import dictConfig
from passlib.hash import pbkdf2_sha256 as sha256
from sklearn.externals import joblib

from flask_app.config import LOGGING_CONFIG, get_config_from_environment
from flask_app.utils import InvalidConfigurationError, InvalidUsage,\
    check_recommend_data_parameters, check_login_parameters, check_score_parameters


def create_app(test_config=None, dummy_test_model=None):
    """
    Create and configure an instance of the Flask basic application

    :param test_config: Configuration dictionary for tests.
    :param dummy_test_model: Dummy model for tests.
    """

    # Define the logging configuration
    dictConfig(LOGGING_CONFIG)

    # Initialize the application
    app = Flask(__name__)

    if test_config is None:
        app.config.update(get_config_from_environment(app.logger))

        if os.environ.get("PROD_SETTINGS", None) is not None:
            app.config.from_envvar("PROD_SETTINGS")
        elif os.environ.get("DEV_SETTINGS", None) is not None:
            app.config.from_envvar("DEV_SETTINGS")

        # Load the model given by the environment variable
        app.logger.info("Getting the machine learning model from the ML_MODEL_PATH " +
                        "environment variable.")
        model_path = os.environ.get("ML_MODEL_PATH", None)
        if model_path is None:
            raise InvalidConfigurationError("The environment variable " +
                                            "\"ML_MODEL_PATH\" doesn't exist. " +
                                            "Please declare it before starting " +
                                            "this application.")
        app.logger.info("Loading model from path %s" % model_path)
        model = joblib.load(model_path)
        app.logger.info("Model successfully loaded")
    else:
        # In case the app is being tested, update the configuration accordingly
        # And use the dummy test model
        app.logger.info("Loading app for testing")
        app.config.update(test_config)
        model = dummy_test_model

    jwt = JWTManager(app)

    @app.route("/")
    def index():
        """
        View to test working server
        """
        return jsonify({"message": "Hello, World!"})

    @app.route("/api/login", methods=["POST"])
    def login():
        # Check the parameters are correct
        data = check_login_parameters(request)

        # Verify the password is valid
        if not sha256.verify(data["session_password"], app.config["SESSION_PASSWORD"]):
            raise InvalidUsage("Incorrect session password", status_code=401)

        # Return the access token
        access_token = create_access_token("session_password")
        return jsonify({"access_token": access_token})

    @app.route("/api/protected", methods=["GET"])
    @jwt_required
    def protected():
        """
        View to test session authentication
        """
        return jsonify({"message": "Protected"})

    @app.route("/api/recommend/score", methods=["POST"])
    @jwt_required
    def score():
        # Check the parameters are correct
        data = check_score_parameters(request)

        # Log the score via the app logger
        data_log = "\nREQUEST SCORE LOG\n"
        data_log += "REQUEST: %s\n" % data["id"]
        data_log += "MOVIE: %s\n" % data["movie"]
        data_log += "SCORE: %.2f" % data["score"]
        app.logger.info(data_log)

        return jsonify("Ok"), 200

    @app.route("/api/recommend", methods=["POST"])
    @jwt_required
    def recommend():
        # Check the parameters are correct
        data = check_recommend_data_parameters(request)

        # Get all the movies of the model (this depends on the model)
        movies = [f.split("=", 1)[1] for f in model.steps[0][1].feature_names_
                  if f.startswith("movie")]

        # Generate a dataset with each movie
        max_recs = data.pop("max_recs", 10)
        X = [{**data, **{"movie": movie}} for movie in movies]

        # Predicts over the whole movie dataset and get the top recommendations
        try:
            recommendations = model.predict(X)
            sorted_recommendations_indices = np.argsort(recommendations)[::-1][:max_recs]
            recommended_movies = [movies[i] for i in sorted_recommendations_indices]

            # Log the valid recommendation and generate an id for it
            request_id = uuid.uuid4()

            data_log = "\nREQUEST RESULT LOG\n"
            data_log += "REQUEST_ID: %s\n" % request_id
            data_log += "DATA: Age=%d Gender=%s Occupation=%s\n" %\
                        (data["age"], data["gender"], data["occupation"])
            data_log += "MOVIES: %s\n" %\
                        ";".join('"%s"' % m.replace('"', '\\"') for m in recommended_movies)
            data_log += "RESULTS: %s" %\
                        ";".join("%.2f" % r for r in recommendations[sorted_recommendations_indices])
            app.logger.info(data_log)

            return jsonify({
                "recommendations": recommended_movies,
                "id": str(request_id)
            })
        except Exception as e:
            app.logger.error("There was an exception while trying to get recommendations: %s" % e)
            app.logger.error("Traceback of the exception:")
            app.logger.exception(e)

            return jsonify({"message": "There was a problem processing your request. Please try again later."}), 500

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    return app
