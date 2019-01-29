# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

import pytest
import uuid


@pytest.fixture
def authentication_headers(client):
    """ Returns a valid token authorization header for the tests of this section to use """
    request_data = {"session_password": "test-password"}
    response = client.post("/api/login", json=request_data)
    access_token = response.get_json()["access_token"]
    headers = {
        "Authorization": "Bearer %s" % access_token
    }

    yield headers


def test_recommend(client, authentication_headers):
    """ Tests the basic recommend request is working correctly (using dummy model) """
    request_data = {"age": 1, "gender": "O", "occupation": "none"}
    response = client.post("/api/recommend", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 200
    assert "recommendations" in response_data
    assert "Test" in response_data["recommendations"]
    assert len(response_data["recommendations"]) == 1
    assert "id" in response_data
    assert len(response_data["id"]) == 36
    assert len(response_data["id"].split("-")) == 5


def test_recommend_age_1(client, authentication_headers):
    """ Tests error on recommend request when 'age' is not present """
    request_data = {"gender": "O", "occupation": "none"}
    response = client.post("/api/recommend", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "age" in response_message


def test_recommend_age_2(client, authentication_headers):
    """ Tests error on recommend request when 'age' is not integer """
    request_data = {"age": "a", "gender": "O", "occupation": "none"}
    response = client.post("/api/recommend", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "parameter" in response_message
    assert "age" in response_message
    assert "integer" in response_message


def test_recommend_gender_1(client, authentication_headers):
    """ Tests error on recommend request when 'gender' is not present """
    request_data = {"age": 1, "occupation": "none"}
    response = client.post("/api/recommend", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "gender" in response_message


def test_recommend_gender_2(client, authentication_headers):
    """ Tests error on recommend request when 'gender' is not valid """
    request_data = {"age": 1, "gender": "G", "occupation": "none"}
    response = client.post("/api/recommend", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "parameter" in response_message
    assert "gender" in response_message
    assert "following" in response_message


def test_recommend_occupation_1(client, authentication_headers):
    """ Tests error on recommend request when 'occupation' is not present """
    request_data = {"age": 1, "gender": "O"}
    response = client.post("/api/recommend", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "occupation" in response_message


def test_recommend_occupation_2(client, authentication_headers):
    """ Tests error on recommend request when 'occupation' is not valid """
    request_data = {"age": 1, "gender": "O", "occupation": "invalid"}
    response = client.post("/api/recommend", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "parameter" in response_message
    assert "occupation" in response_message
    assert "following" in response_message


def test_recommend_max_recs(client, authentication_headers):
    """ Tests error on recommend request when 'max_recs' is not integer """
    request_data = {"age": 1, "gender": "O", "occupation": "none", "max_recs": "none"}
    response = client.post("/api/recommend", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "parameter" in response_message
    assert "max_recs" in response_message
    assert "integer" in response_message


def test_recommend_invalid_param(client, authentication_headers):
    """ Tests error on recommend request with invalid parameter """
    request_data = {"age": 1, "gender": "O", "occupation": "none", "extra": 0}
    response = client.post("/api/recommend", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "only" in response_message
    assert "valid" in response_message
    assert "parameters" in response_message


def test_score(client, authentication_headers):
    request_data = {"id": str(uuid.uuid4()), "movie": "Test", "score": 1}
    response = client.post("/api/recommend/score", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 200
    assert response_data == "Ok"


def test_score_id_1(client, authentication_headers):
    request_data = {"movie": "Test", "score": 1}
    response = client.post("/api/recommend/score", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "id" in response_message


def test_score_id_2(client, authentication_headers):
    request_data = {"id": "invalid", "movie": "Test", "score": 1}
    response = client.post("/api/recommend/score", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "invalid" in response_message
    assert "parameter" in response_message
    assert "id" in response_message


def test_score_id_3(client, authentication_headers):
    request_data = {"id": "i" * 36, "movie": "Test", "score": 1}
    response = client.post("/api/recommend/score", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "invalid" in response_message
    assert "parameter" in response_message
    assert "id" in response_message


def test_score_movie_1(client, authentication_headers):
    request_data = {"id": str(uuid.uuid4()), "score": 1}
    response = client.post("/api/recommend/score", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "movie" in response_message


def test_score_score_1(client, authentication_headers):
    request_data = {"id": str(uuid.uuid4()), "movie": "Test"}
    response = client.post("/api/recommend/score", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "score" in response_message


def test_score_score_2(client, authentication_headers):
    request_data = {"id": str(uuid.uuid4()), "movie": "Test", "score": "a"}
    response = client.post("/api/recommend/score", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "parameter" in response_message
    assert "score" in response_message
    assert "valid" in response_message
    assert "number" in response_message


def test_score_score_3(client, authentication_headers):
    request_data = {"id": str(uuid.uuid4()), "movie": "Test", "score": 5.5}
    response = client.post("/api/recommend/score", json=request_data, headers=authentication_headers)

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "parameter" in response_message
    assert "score" in response_message
    assert "interval" in response_message
