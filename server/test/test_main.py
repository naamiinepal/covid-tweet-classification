from typing import Mapping, Union
from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_index():
    for path in ("/", "/index.html"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"


def test_robots():
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/plain; charset=utf-8"


def test_favicon():
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/vnd.microsoft.icon"


def asset_manifest():
    response = client.get("/asset-manifest.json")
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response.get("files"), dict)
    assert isinstance(json_response.get("entrypoints"), list)
