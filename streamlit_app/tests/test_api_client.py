import pytest
import httpx
import respx
import sys
import os

# Add the parent directory to sys.path so we can import streamlit_app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from streamlit_app.api_client import api, APIError

import re

@respx.mock
def test_login_success():
    respx.post(re.compile(r".*/auth/login")).mock(return_value=httpx.Response(200, json={"access_token": "fake_token", "token_type": "bearer"}))
    token_data = api.login("test@test.com", "password")
    assert "access_token" in token_data
    assert token_data["access_token"] == "fake_token"

@respx.mock
def test_login_failure():
    respx.post(re.compile(r".*/auth/login")).mock(return_value=httpx.Response(401, json={"detail": "Incorrect username or password"}))
    with pytest.raises(APIError) as excinfo:
        api.login("wrong@test.com", "wrongpassword")
    assert "Incorrect username or password" in str(excinfo.value)
    assert excinfo.value.status_code == 401

@respx.mock
def test_get_transactions_success():
    mock_data = [{"id": 1, "amount": 100.0, "description": "Test"}]
    req = respx.get(re.compile(r".*/transactions/?\?.*")).mock(return_value=httpx.Response(200, json=mock_data))
    
    response = api.get_transactions("fake_token")
    assert len(response) == 1
    assert response[0]["amount"] == 100.0
    assert req.called

@respx.mock
def test_create_transaction_success():
    mock_response = {"id": 1, "amount": 50.0, "description": "Food"}
    req = respx.post(re.compile(r".*/transactions/.*")).mock(return_value=httpx.Response(201, json=mock_response))
    
    response = api.create_transaction("fake_token", amount=50.0, description="Food", category_id=None)
    assert response["id"] == 1
    assert response["amount"] == 50.0
    assert req.called

@respx.mock
def test_delete_transaction():
    req = respx.delete(re.compile(r".*/transactions/1")).mock(return_value=httpx.Response(204))
    success = api.delete_transaction("fake_token", 1)
    assert success is True
    assert req.called
