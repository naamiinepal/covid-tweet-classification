from glob import glob
from . import client


def test_index():
    for path in ("/", "/index.html"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")


def test_robots():
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")


def test_favicon():
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("image/vnd.microsoft.icon")


def test_asset_manifest():
    response = client.get("/asset-manifest.json")
    assert response.status_code == 200
    json_response = response.json()
    assert isinstance(json_response.get("files"), dict)
    assert isinstance(json_response.get("entrypoints"), list)


def _test_static_files(file_pattern: str, content_type: str):
    for path in glob(file_pattern):
        response = client.get(path)
        assert response.status_code == 200
        assert response.headers["content-type"].startswith(content_type)


def test_javascript():
    _test_static_files("static/js/*.js", "application/javascript")


def test_css():
    _test_static_files("static/css/*.js", "text/css")
