from fastapi.testclient import TestClient

from src.dependencies import get_session
from src.main import app
from src.tests.conftest import get_test_session

client = TestClient(app)
app.dependency_overrides[get_session] = get_test_session


def test_get_flights_method(create_models):
    response = client.get("/flights/2022-01-01")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "file_name": "test_file1.csv", "flt": 1234, "depdate": "2022-01-01", "dep": "test1"},
    ]
