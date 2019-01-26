# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest


def test_index(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "message" in response.get_json()
