# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest

from flask_app.app import create_app
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
    app = create_app({'TESTING': True}, get_dummy_test_model())
    client = app.test_client()

    yield client

