# Flask Auth Demo API

## Project purpose
This is a small beginner-friendly Flask REST API that demonstrates:
- login with username/password
- token refresh flow
- accessing a protected profile endpoint

It uses in-memory demo users and in-memory tokens so it stays easy to explain live.

## Setup instructions
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to run the application
```bash
python app.py
```
The API runs at `http://127.0.0.1:5000` by default.

## How to run tests
```bash
pytest
```

## API endpoints
- `POST /login`
- `POST /auth/refresh`
- `GET /profile`

## Contribution instructions
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for beginner-friendly contribution steps.
