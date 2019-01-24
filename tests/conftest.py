# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest

from flask_app.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

