# Portfolio Manager Frontend

This is the React frontend for the Portfolio Manager application.

## Prerequisites
- Node.js (version 18+)
- npm
- A running Flask backend at `http://localhost:5000`
- An AWS Cognito User Pool configured for authentication

## Installation
From the `frontend` directory, install dependencies:
```bash
npm install
```

## Environment Configuration
Copy `.env.example` to `.env` and fill in the values from your AWS Cognito User Pool:
```bash
cp .env.example .env
```

Required variables:
- `VITE_COGNITO_AUTHORITY`: The authority URL for Cognito
- `VITE_COGNITO_CLIENT_ID`: The app client ID
- `VITE_COGNITO_DOMAIN`: The Cognito domain for the Hosted UI
- `VITE_COGNITO_REDIRECT_URI`: Should be `http://localhost:5173/callback`
- `VITE_COGNITO_LOGOUT_URI`: Should be `http://localhost:5173/`
- `VITE_COGNITO_SCOPE`: OpenID Connect scopes (`openid email profile`)
- `VITE_API_BASE_URL`: The URL of the backend (e.g., `http://localhost:5000`)

## Running Locally
Start the Vite dev server:
```bash
npm run dev
```
The server will run on port 5173.

## Building for Production
```bash
npm run build
npm run preview
```

## Cognito Configuration Requirements
Your Cognito User Pool must have:
- App client type: Single-page application (public, no client secret)
- Authorization code grant enabled
- Allowed callback URL: `http://localhost:5173/callback`
- Allowed sign-out URL: `http://localhost:5173/`
- OpenID Connect scopes: `openid`, `email`, `profile`

## Project Structure
- `src/api/`: API clients to communicate with the Flask backend.
- `src/auth/`: OIDC Authentication wiring and hooks.
- `src/components/`: Reusable React components (forms, tables, etc.).
- `src/pages/`: Main page layouts (Login, Portfolios, Detail).
- `src/App.jsx`: Main application routing.
- `src/main.jsx`: Application entry point.
- `src/index.css`: Global styles.

## Features
- OIDC Authentication using AWS Cognito
- View, Create, and Delete portfolios
- View holdings and transaction history per portfolio
- Execute Buy and Sell trades

## Known Limitations
- Logout uses Cognito's logout endpoint, which terminates the session globally. After logout the user lands on `/`, which redirects to `/login`.
