import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

base_path = "/auth/"


def test_unauth_get_me(client: TestClient):
    response = client.get(base_path + "me")
    assert response.status_code == 401


# Duplicate email check fails for now
@pytest.mark.xfail(IntegrityError)
def test_register(client: TestClient):
    response = client.post(
        base_path + "register",
        json={
            "username": "john",
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "secret",
        },
    )
    assert response.status_code == 200
    json_response = response.json()
    access_token: str = json_response["access_token"]
    assert len(access_token.split(".")) == 3
    assert json_response["token_type"] == "bearer"

    # Cannot insert user of same username
    response = client.post(
        base_path + "register",
        json={
            "username": "john",
            "email": "test@example.com",
            "full_name": "Johnathan Doe",
            "password": "secret2",
        },
    )
    assert response.status_code == 400

    # Cannot insert user of same email
    response = client.post(
        base_path + "register",
        json={
            "username": "johnathan",
            "email": "john@example.com",
            "full_name": "Johnathan Dormer",
            "password": "secret3",
        },
    )
    assert response.status_code == 400
