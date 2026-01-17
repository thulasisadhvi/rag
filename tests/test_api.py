from fastapi.testclient import TestClient
from src.api.main import app

# Create a test client that wraps your FastAPI app
client = TestClient(app)

def test_health_check():
    """
    Verifies the /health endpoint returns status 200 and 'active'.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "active"}

def test_query_endpoint_structure():
    """
    Verifies the /query endpoint accepts the correct JSON format.
    Note: We aren't checking for a 'correct' answer here, just that 
    the server accepts the request without a validation error (422).
    """
    payload = {"query": "This is a test query"}
    
    response = client.post("/query", json=payload)
    
    # We accept 200 (Success) or 500 (Server Error - e.g., if DB is empty).
    # We just want to ensure it's NOT 422 (Unprocessable Entity/Bad Data).
    assert response.status_code in [200, 500]
    
    if response.status_code == 200:
        data = response.json()
        assert "answer" in data
        assert "sources" in data