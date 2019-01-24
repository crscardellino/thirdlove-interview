# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest


def test_index(client):
    response = client.get("/")
    json_data = response.get_json()
    assert "message" in json_data
