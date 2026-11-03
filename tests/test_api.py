from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_document_returns_id_and_length():
    response = client.post("/documents", json={"text": "hello world"})
    assert response.status_code == 200
    body = response.json()
    assert body["length"] == 11
    assert body["id"]


def test_create_document_rejects_empty_text():
    response = client.post("/documents", json={"text": "   "})
    assert response.status_code == 400


def test_get_missing_document_returns_404():
    response = client.get("/documents/does-not-exist")
    assert response.status_code == 404


def test_roundtrip_create_then_fetch():
    created = client.post("/documents", json={"text": "some text"}).json()
    fetched = client.get(f"/documents/{created['id']}").json()
    assert fetched["id"] == created["id"]
    assert fetched["length"] == 9

def test_index_page_is_served():
    response = client.get("/")
    assert response.status_code == 200
    assert "Document service" in response.text