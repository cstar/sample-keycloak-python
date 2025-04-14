from flask import Flask, redirect, url_for, session, request, jsonify
from keycloak import KeycloakOpenID
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')

# Keycloak configuration
keycloak_openid = KeycloakOpenID(
    server_url=os.getenv('KEYCLOAK_SERVER_URL', 'http://localhost:8080/auth/'),
    client_id=os.getenv('KEYCLOAK_CLIENT_ID', 'your-client-id'),
    realm_name=os.getenv('KEYCLOAK_REALM', 'your-realm'),
    client_secret_key=os.getenv('KEYCLOAK_CLIENT_SECRET', 'your-client-secret')
)

@app.route('/')
def index():
    if 'token' in session:
        return 'Welcome! You are logged in. <a href="/logout">Logout</a>'
    return 'Welcome! <a href="/login">Login</a>'

@app.route('/login')
def login():
    # Get the authorization URL
    auth_url = keycloak_openid.auth_url(
        redirect_uri=url_for('callback', _external=True),
        scope='openid'
    )
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Get the authorization code from the callback
    code = request.args.get('code')
    if not code:
        return 'Authorization failed', 401

    try:
        # Get the token
        token = keycloak_openid.token(
            grant_type='authorization_code',
            code=code,
            redirect_uri=url_for('callback', _external=True)
        )
        
        # Store the token in the session
        session['token'] = token
        
        # Get user info
        userinfo = keycloak_openid.userinfo(token['access_token'])
        session['userinfo'] = userinfo
        
        return redirect(url_for('protected'))
    except Exception as e:
        return f'Authentication failed: {str(e)}', 401

@app.route('/logout')
def logout():
    if 'token' in session:
        try:
            # Logout from Keycloak
            keycloak_openid.logout(session['token']['refresh_token'])
        except Exception:
            pass
        session.clear()
    return redirect(url_for('index'))

@app.route('/protected')
def protected():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    try:
        # Verify the token
        keycloak_openid.introspect(session['token']['access_token'])
        return jsonify({
            'message': 'This is a protected endpoint',
            'user_info': session.get('userinfo')
        })
    except Exception as e:
        return f'Token validation failed: {str(e)}', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 