from datetime import datetime, timedelta, timezone
from functools import wraps
from secrets import token_urlsafe

from flask import Flask, jsonify, request

app = Flask(__name__)

# Demo users are hard-coded for learning purposes only.
# These are NOT real credentials and should never be used in production.
DEMO_USERS = {
    "alice": {"password": "password123", "name": "Alice Example", "email": "alice@example.com"},
    "bob": {"password": "password456", "name": "Bob Example", "email": "bob@example.com"},
}

# In-memory token stores. This keeps the project simple for beginners.
ACCESS_TOKENS = {}
REFRESH_TOKENS = {}
ACCESS_TOKEN_TTL = timedelta(minutes=5)
REFRESH_TOKEN_TTL = timedelta(hours=1)


def utc_now():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)


def issue_access_token(username):
    """Create and store a short-lived access token for a user."""
    token = token_urlsafe(24)
    ACCESS_TOKENS[token] = {"username": username, "expires_at": utc_now() + ACCESS_TOKEN_TTL}
    return token


def issue_refresh_token(username):
    """Create and store a longer-lived refresh token for a user."""
    token = token_urlsafe(32)
    REFRESH_TOKENS[token] = {"username": username, "expires_at": utc_now() + REFRESH_TOKEN_TTL}
    return token


def require_access_token(route):
    """Simple auth decorator that checks for a valid bearer token."""

    @wraps(route)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = auth_header.removeprefix("Bearer ").strip()

        if not token:
            return jsonify({"error": "Missing bearer token"}), 401

        token_record = ACCESS_TOKENS.get(token)
        if not token_record or token_record["expires_at"] < utc_now():
            return jsonify({"error": "Invalid or expired access token"}), 401

        return route(token_record["username"], *args, **kwargs)

    return wrapper


@app.post("/login")
def login():
    """Authenticate a demo user and return new tokens."""
    payload = request.get_json(silent=True) or {}
    username = payload.get("username", "")
    password = payload.get("password", "")

    user = DEMO_USERS.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify(
        {
            "access_token": issue_access_token(username),
            "refresh_token": issue_refresh_token(username),
            "token_type": "Bearer",
        }
    )


@app.post("/auth/refresh")
def refresh():
    """Exchange a valid refresh token for a new access token."""
    payload = request.get_json(silent=True) or {}
    refresh_token = payload.get("refresh_token", "")
    token_record = REFRESH_TOKENS.get(refresh_token)

    if not token_record or token_record["expires_at"] < utc_now():
        return jsonify({"error": "Invalid or expired refresh token"}), 401

    return jsonify({"access_token": issue_access_token(token_record["username"]), "token_type": "Bearer"})


@app.get("/profile")
@require_access_token
def profile(username):
    """Return a small profile object for the authenticated demo user."""
    user = DEMO_USERS[username]
    return jsonify({"username": username, "name": user["name"], "email": user["email"]})


if __name__ == "__main__":
    # Keep debug disabled by default for safer local demos.
    app.run()
