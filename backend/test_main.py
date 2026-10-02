from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_books():
    response = client.get("/books")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_members():
    response = client.get("/members")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_transactions():
    response = client.get("/transactions")

    assert response.status_code == 200
    assert isinstance(response.json(), list)