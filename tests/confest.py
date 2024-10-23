import pytest
from fastapi.testclient import TestClient
from app.main import app  # Adjust the import to your main FastAPI app

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client