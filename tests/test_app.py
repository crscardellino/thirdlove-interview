# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest


def test_index(client):
    """ Tests the basic application """
    response = client.get("/")

    response_data = response.get_json()
    assert response.status_code == 200
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "hello" in response_message
    assert "world" in response_message

