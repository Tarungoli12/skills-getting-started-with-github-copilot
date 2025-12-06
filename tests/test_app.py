from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # ensure at least one known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure email is not present first (tests may run repeatedly)
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    if email in participants:
        client.post(f"/activities/{activity}/unregister?email={email}")

    # Sign up the test email
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    # Confirm participant present
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    assert email in participants

    # Unregister the test email
    res = client.post(f"/activities/{activity}/unregister?email={email}")
    assert res.status_code == 200
    assert "Unregistered" in res.json().get("message", "")

    # Confirm participant removed
    res = client.get("/activities")
    participants = res.json()[activity]["participants"]
    assert email not in participants
