from fastapi.testclient import TestClient
from requests import Response
from sqlmodel import Session

from app.auth.helper_functions import get_password_hash
from app.auth.models import User

base_path = "/auth/"

register_path = base_path + "register"
login_path = base_path + "login"


def verify_access_token(response: Response):
    json_response = response.json()
    access_token: str = json_response["access_token"]
    assert len(access_token.split(".")) == 3
    assert json_response["token_type"] == "bearer"


def test_unauth_get_me(client: TestClient):
    response = client.get(base_path + "me")
    assert response.status_code == 401


def test_register(client: TestClient):
    response = client.post(
        register_path,
        json={
            "username": "john",
            "email": "john@example.com",
            "full_name": "John Doe",
            "password": "secret",
        },
    )
    assert response.status_code == 200
    verify_access_token(response)

    # Cannot insert user of same username
    response = client.post(
        register_path,
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
        register_path,
        json={
            "username": "johnathan",
            "email": "john@example.com",
            "full_name": "Johnathan Dormer",
            "password": "secret3",
        },
    )
    assert response.status_code == 400


def test_login(client: TestClient, session: Session):
    password = "secret"
    user = User(
        username="john",
        email="john@example.com",
        full_name="Johnathan Dormer",
        hashed_password=get_password_hash(password),
    )
    session.add(user)
    session.commit()

    response = client.post(
        login_path,
        {"username": user.username, "password": password},
    )

    assert response.status_code == 200

    verify_access_token(response)

    # Incorrect Password
    response = client.post(
        login_path,
        {"username": user.username, "password": "hashed_password"},
    )

    assert response.status_code == 400


def test_unauth_login(client: TestClient):
    response = client.post(
        login_path,
        {"username": "john", "password": "secret4"},
    )

    assert response.status_code == 400
