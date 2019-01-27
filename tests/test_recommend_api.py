# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import json
import pytest


def test_recommend(client):
    """ Tests the basic recommend request is working correctly (using dummy model) """
    request_data = {"age": 1, "gender": "O", "occupation": "none"}
    response = client.post("/api/recommend", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 200
    assert "recommendations" in response_data
    assert "Test" in response_data["recommendations"]
    assert len(response_data["recommendations"]) == 1


def test_recommend_age_1(client):
    """ Tests error on recommend request when 'age' is not present """
    request_data = {"gender": "O", "occupation": "none"}
    response = client.post("/api/recommend", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "age" in response_message


def test_recommend_age_2(client):
    """ Tests error on recommend request when 'age' is not integer """
    request_data = {"age": "a", "gender": "O", "occupation": "none"}
    response = client.post("/api/recommend", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "parameter" in response_message
    assert "age" in response_message
    assert "integer" in response_message


def test_recommend_gender_1(client):
    """ Tests error on recommend request when 'gender' is not present """
    request_data = {"age": 1, "occupation": "none"}
    response = client.post("/api/recommend", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "gender" in response_message


def test_recommend_gender_2(client):
    """ Tests error on recommend request when 'gender' is not valid """
    request_data = {"age": 1, "gender": "G", "occupation": "none"}
    response = client.post("/api/recommend", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "parameter" in response_message
    assert "gender" in response_message
    assert "following" in response_message


def test_recommend_occupation_1(client):
    """ Tests error on recommend request when 'occupation' is not present """
    request_data = {"age": 1, "gender": "O"}
    response = client.post("/api/recommend", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "occupation" in response_message


def test_recommend_occupation_2(client):
    """ Tests error on recommend request when 'occupation' is not valid """
    request_data = {"age": 1, "gender": "O", "occupation": "invalid"}
    response = client.post("/api/recommend", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "parameter" in response_message
    assert "occupation" in response_message
    assert "following" in response_message


def test_recommend_invalid_param(client):
    """ Tests error on recommend request with invalid parameter """
    request_data = {"age": 1, "gender": "O", "occupation": "none", "extra": 0}
    response = client.post("/api/recommend", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "only" in response_message
    assert "valid" in response_message
    assert "parameters" in response_message
