from fastapi.testclient import TestClient
from main import app  # Importa tu aplicación FastAPI

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "¡FastAPI funciona!"}