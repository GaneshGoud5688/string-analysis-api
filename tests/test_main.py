from fastapi.testclient import TestClient
from main import app
from config import MAX_INPUT_SIZE

client = TestClient(app)

def test_valid_json_input():
    response = client.post(
        "/analyze?analyses=word_count&analyses=char_count",
        json={"text": "Hello world!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["results"]["word_count"] == 2
    assert data["results"]["char_count"] == len("Hello world!")


def test_valid_plain_text_input():
    response = client.post(
        "/analyze?analyses=word_count&analyses=unique_words",
        data="Hello hello world!",
        headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["results"]["word_count"] == 3
    assert data["results"]["unique_words"] == 2


def test_missing_body():
    response = client.post("/analyze?analyses=word_count")
    assert response.status_code == 400
    assert "Empty request body" in response.text


def test_invalid_json():
    response = client.post(
        "/analyze?analyses=word_count",
        data='{"text": "unclosed',
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
    assert "Invalid JSON" in response.text


def test_input_too_large():
    large_text = "a" * (MAX_INPUT_SIZE + 1)
    response = client.post(
        "/analyze?analyses=char_count",
        json={"text": large_text}
    )
    assert response.status_code == 413
    assert "character limit" in response.text


def test_unsupported_analysis():
    response = client.post(
        "/analyze?analyses=invalid_analysis",
        json={"text": "Hello world"}
    )
    assert response.status_code in (400, 500)
    assert "Unsupported analysis type" in response.text
