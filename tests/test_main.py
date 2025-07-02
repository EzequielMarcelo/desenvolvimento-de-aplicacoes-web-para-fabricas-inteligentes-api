import sys
import os
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from main import app

client = TestClient(app)

def test_post_temperatura():
    response = client.post("/temperatura", json={"temperatura": 10.0})
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_temperatura():
    response = client.get("/temperatura")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_post_e_get_temperatura():
    response_post = client.post("/temperatura", json={"temperatura": 25.0})
    assert response_post.status_code == 200

    response_get = client.get("/temperatura")
    assert response_get.status_code == 200
    dados = response_get.json()

    assert any(item["valor"] == 25.0 for item in dados)
