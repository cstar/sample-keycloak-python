# Flask Keycloak OIDC Authentication

This is a Flask application that demonstrates OIDC authentication using Keycloak.

## Prerequisites

- Python 3.8 or higher
- A running Keycloak server
- A configured Keycloak client with OIDC enabled

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy the environment file and configure it:
```bash
cp .env.example .env
```

4. Edit the `.env` file with your Keycloak configuration:
- `FLASK_SECRET_KEY`: A secure random string for Flask session encryption
- `KEYCLOAK_SERVER_URL`: Your Keycloak server URL (e.g., http://localhost:8080/auth/)
- `KEYCLOAK_CLIENT_ID`: Your Keycloak client ID
- `KEYCLOAK_REALM`: Your Keycloak realm name
- `KEYCLOAK_CLIENT_SECRET`: Your Keycloak client secret

## Running the Application

1. Start the Flask development server:
```bash
python app.py
```

2. The application will be available at `http://localhost:5000`

## Keycloak Client Configuration

Make sure your Keycloak client is configured with:
- Access Type: confidential
- Valid Redirect URIs: http://localhost:5000/callback
- Web Origins: http://localhost:5000

## Endpoints

- `/`: Home page with login/logout links
- `/login`: Initiates the OIDC login flow
- `/logout`: Logs out the user
- `/protected`: A protected endpoint that requires authentication
