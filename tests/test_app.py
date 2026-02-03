import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data


def test_signup_for_activity_success():
    response = client.post("/activities/Basketball Team/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up tester@mergington.edu for Basketball Team" in response.json().get("message", "")


def test_signup_for_activity_duplicate():
    # Sign up once
    client.post("/activities/Drama Club/signup?email=repeat@mergington.edu")
    # Try to sign up again
    response = client.post("/activities/Drama Club/signup?email=repeat@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")


def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json().get("detail", "")


def test_unregister_participant_success():
    # First, sign up
    client.post("/activities/Chess Club/signup?email=remove@mergington.edu")
    # Then, unregister
    response = client.post("/activities/Chess Club/unregister?email=remove@mergington.edu")
    assert response.status_code == 200
    assert "Removed remove@mergington.edu from Chess Club" in response.json().get("message", "")


def test_unregister_nonexistent_participant():
    response = client.post("/activities/Art Workshop/unregister?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Participant not found" in response.json().get("detail", "")
