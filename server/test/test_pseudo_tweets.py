from . import client

base_path = "/tweets/pseudo/"


def test_overview():
    response = client.get(base_path + "overview")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_tweets():
    response = client.get(base_path)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
