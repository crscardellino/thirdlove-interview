# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals

from time import sleep

from tests.utils import get_test_client


def test_authentication(client):
    """ Tests the basic authentication """
    request_data = {"session_password": "test-password"}
    response = client.post("/api/login", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in response_data

    access_token = response_data["access_token"]
    headers = {
        "Authorization": "Bearer %s" % access_token
    }

    response = client.get("/api/protected", headers=headers)

    response_data = response.get_json()
    assert response.status_code == 200
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "protected" in response_message


def test_missing_header(client):
    """ Test requests without headers are errors"""
    response = client.get("/api/protected")

    response_data = response.get_json()
    assert response.status_code == 401
    assert "msg" in response_data

    response_message = response_data["msg"].lower()
    assert "missing" in response_message
    assert "authorization" in response_message
    assert "header" in response_message


def test_unauthorized(client):
    """ Test unauthorized requests are errors """
    # First get a valid token that will be modified
    request_data = {"session_password": "test-password"}
    response = client.post("/api/login", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in response_data

    # Modify the access_token
    access_token = response_data["access_token"][:-1] + "1"
    headers = {
        "Authorization": "Bearer %s" % access_token
    }

    response = client.get("/api/protected", headers=headers)
    response_data = response.get_json()
    assert response.status_code == 422
    assert "msg" in response_data

    response_message = response_data["msg"].lower()
    assert "signature" in response_message
    assert "verification" in response_message
    assert "failed" in response_message


def test_missing_password(client):
    """ Tests the missing password is an error """
    response = client.post("/api/login", json={})

    response_data = response.get_json()
    assert response.status_code == 400
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "missing" in response_message
    assert "parameter" in response_message
    assert "session_password" in response_message


def test_wrong_password(client):
    """ Tests the wrong password is an error """
    request_data = {"session_password": "test-password-1"}
    response = client.post("/api/login", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 401
    assert "message" in response_data

    response_message = response_data["message"].lower()
    assert "incorrect" in response_message
    assert "session" in response_message
    assert "password" in response_message


def test_token_expiration():
    """ Test requests with expired tokens are errors """
    client = get_test_client(1)  # Get special client with short token expiration time
    # First get a valid token
    request_data = {"session_password": "test-password"}
    response = client.post("/api/login", json=request_data)

    response_data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in response_data

    # Wait for the token to expire
    sleep(2)
    access_token = response_data["access_token"]
    headers = {
        "Authorization": "Bearer %s" % access_token
    }

    response = client.get("/api/protected", headers=headers)
    response_data = response.get_json()
    assert response.status_code == 401
    assert "msg" in response_data

    response_message = response_data["msg"].lower()
    assert "token" in response_message
    assert "expired" in response_message
