# -*- coding: utf-8 -*-
# Creator: Cristian Cardellino

from __future__ import absolute_import

import datetime

from passlib.hash import pbkdf2_sha256 as sha256
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

from flask_app.app import create_app


def get_dummy_test_model():
    """
    Returns a dummy model pipeline with the solely purpose of using it for tests.
    """
    model = make_pipeline(DictVectorizer(), LinearRegression())
    model.fit([{"age": 1, "gender": "O", "occupation": "None", "movie": "Test"}], [0])

    return model


def get_test_client(jwt_expiration_time=3600):
    """
    Returns a client for testing purposes.
    :param jwt_expiration_time: Set the expiration time (in seconds) for the JWT tokens.
    :return: Application's test client
    """
    config = {
        "TESTING": True,
        "SESSION_PASSWORD": sha256.hash("test-password"),
        "SECRET_KEY": "test-secret-key",
        "JWT_SECRET_KEY": "test-secret-key",
        "JWT_ACCESS_TOKEN_EXPIRES": datetime.timedelta(seconds=jwt_expiration_time)
    }

    return create_app(config, get_dummy_test_model()).test_client()
