# Portfolio Management Application

This is a Flask app built for managing portfolios, placing buy/sell trades, and tracking transaction history.

It uses Alpha Vantage for market prices and Cognito-style token auth for protected routes.

## What It Does

- Create and manage users with balances
- Create portfolios and list portfolio data
- Execute buy and sell operations
- Track transaction history
- Enforce access checks on protected actions

## Tech Stack

- Python + Flask
- SQLAlchemy ORM
- Pydantic request validation
- Flask-Caching
- pytest + coverage

## Quick Start

1. Create and activate a virtual environment.

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Create a `.env` (or set environment variables) with your config.

```env
FLASK_ENV=development
DATABASE_URL=mysql+pymysql://user:password@localhost/dbname
ALPHA_VANTAGE_API_KEY=your_api_key_here
COGNITO_REGION=us-east-1
COGNITO_USER_POOL_ID=your_pool_id
COGNITO_APP_CLIENT_ID=your_client_id
COGNITO_JWKS_URL=https://cognito-idp.<region>.amazonaws.com/<pool_id>/.well-known/jwks.json
```

## Run the App

Use the project venv interpreter so imports/dependencies are consistent.

```bash
venv\Scripts\python.exe app\main.py
```

Default local URL: `http://127.0.0.1:5000`

## Run Tests + Coverage

```bash
venv\Scripts\python.exe -m pytest --cov=app --cov-report=term-missing
```

Current benchmark status:
- All tests passing
- Coverage is above 80%

## Main Routes

- `GET /securities/` (auth required)
- `GET /securities/<ticker>` (auth required)
- `GET /securities/<ticker>/transactions` (auth required)
- `GET /users/` (auth required)
- `POST /users/` (auth required)
- `GET /portfolios/` (auth required)
- `POST /portfolios/` (auth required)
- `POST /trades/buy` (auth + access check)
- `POST /trades/sell` (auth + access check)

## Project Layout

```text
app/
  auth/         authentication helpers/decorators
  models/       SQLAlchemy models
  routes/       Flask blueprints
  service/      business logic
  schemas.py    pydantic request schemas
  config.py     app config classes
  main.py       entry point
```

## Notes

- `python app/main.py` and `python -m app.main` can behave differently depending on your interpreter/path.
- If you hit module errors, run everything through `venv\Scripts\python.exe`.