import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity_success():
    # Use a unique email to avoid duplicate error
    response = client.post("/activities/Art Club/signup?email=testuser1@mergington.edu")
    assert response.status_code == 200
    assert "Signed up testuser1@mergington.edu for Art Club" in response.json()["message"]


def test_signup_for_activity_duplicate():
    # First signup
    client.post("/activities/Drama Club/signup?email=testuser2@mergington.edu")
    # Duplicate signup
    response = client.post("/activities/Drama Club/signup?email=testuser2@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=testuser3@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
