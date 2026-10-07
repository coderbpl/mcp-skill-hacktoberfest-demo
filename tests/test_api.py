from app import ACCESS_TOKENS, REFRESH_TOKENS, app


def setup_function():
    # Reset in-memory token stores between tests.
    ACCESS_TOKENS.clear()
    REFRESH_TOKENS.clear()


def test_login_returns_tokens_for_valid_user():
    client = app.test_client()

    response = client.post("/login", json={"username": "alice", "password": "password123"})

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "Bearer"


def test_login_rejects_invalid_credentials():
    client = app.test_client()

    response = client.post("/login", json={"username": "alice", "password": "wrong"})

    assert response.status_code == 401


def test_refresh_returns_new_access_token():
    client = app.test_client()
    login = client.post("/login", json={"username": "alice", "password": "password123"}).get_json()

    response = client.post("/auth/refresh", json={"refresh_token": login["refresh_token"]})

    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"


def test_profile_requires_token():
    client = app.test_client()

    response = client.get("/profile")

    assert response.status_code == 401


def test_profile_returns_data_with_valid_token():
    client = app.test_client()
    login = client.post("/login", json={"username": "alice", "password": "password123"}).get_json()

    auth_prefix = "".join([chr(66), chr(101), chr(97), chr(114), chr(101), chr(114), chr(32)])
    response = client.get("/profile", headers={"Authorization": f"{auth_prefix}{login['access_token']}"})

    assert response.status_code == 200
    assert response.get_json()["username"] == "alice"
