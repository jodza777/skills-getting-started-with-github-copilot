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
    assert "participants" in data["Chess Club"]

def test_signup_and_remove_participant():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/participants/{email}")
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    # Remove participant
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert f"Removed {email} from {activity}" in response.json()["message"]
    # Removing again should fail
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=foo@bar.com")
    assert response.status_code == 404

def test_remove_nonexistent_participant():
    response = client.delete("/activities/Chess Club/participants/notfound@mergington.edu")
    assert response.status_code == 404

