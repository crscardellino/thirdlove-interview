# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import datetime
import pytest

from flask_app.app import create_app
from passlib.hash import pbkdf2_sha256 as sha256
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline


def get_dummy_test_model():
    """
    Returns a dummy model pipeline with the solely purpose of using it for tests.
    """
    model = make_pipeline(DictVectorizer(), LinearRegression())
    model.fit([{"age": 1, "gender": "O", "occupation": "None", "movie": "Test"}], [0])

    return model


@pytest.fixture
def client():
    config = {
        "TESTING": True,
        "SESSION_PASSWORD": sha256.hash("test-password"),
        "SECRET_KEY": "test-secret-key",
        "JWT_SECRET_KEY": "test-secret-key",
        "JWT_ACCESS_TOKEN_EXPIRES": datetime.timedelta(seconds=1)
    }
    app = create_app(config, get_dummy_test_model())
    client = app.test_client()

    yield client

