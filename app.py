from flask import Flask, render_template, redirect, url_for, session, request
from auth import auth0, init_auth
import os
import logging
from datetime import datetime
from functools import wraps
from urllib.parse import quote_plus, urlencode

app = Flask(__name__)
app.secret_key = os.getenv('AUTH0_SECRET')

# Initialize Auth0
init_auth(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add structured logging
class StructuredLogger:
    @staticmethod
    def log_event(event_type, user_id=None, email=None, route=None, status=None, extra=None):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "email": email,
            "route": route,
            "status": status,
            "extra": extra or {}
        }
        logger.info(f"SECURITY_EVENT: {log_entry}")
        return log_entry

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = session.get('user')
        if not user:
            StructuredLogger.log_event(
                "unauthorized_access",
                route=request.path,
                status="denied"
            )
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    user = session.get('user')
    if user:
        StructuredLogger.log_event(
            "page_view",
            user_id=user.get('sub'),
            email=user.get('email'),
            route='/'
        )
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    StructuredLogger.log_event("login_attempt", route='/login')
    return auth0.authorize_redirect(
        redirect_uri=url_for('callback', _external=True)
    )

@app.route('/callback')
def callback():
    try:
        # Get the token
        token = auth0.authorize_access_token()
        
        # Get user info
        resp = auth0.get('userinfo', token=token)
        userinfo = resp.json()
        
        # Store user in session
        session['user'] = userinfo
        
        StructuredLogger.log_event(
            "login_success",
            user_id=userinfo.get('sub'),
            email=userinfo.get('email'),
            status="success"
        )
        return redirect(url_for('index'))
    except Exception as e:
        StructuredLogger.log_event(
            "login_failure",
            route='/callback',
            status="failed",
            extra={"error": str(e)}
        )
        return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    user = session.get('user')
    StructuredLogger.log_event(
        "protected_access",
        user_id=user.get('sub'),
        email=user.get('email'),
        route='/profile',
        status="accessed"
    )
    return render_template('profile.html', user=user)

@app.route('/protected')
@login_required
def protected():
    user = session.get('user')
    StructuredLogger.log_event(
        "protected_access",
        user_id=user.get('sub'),
        email=user.get('email'),
        route='/protected',
        status="accessed"
    )
    return render_template('protected.html', user=user)

@app.route('/logout')
def logout():
    user = session.get('user')
    if user:
        StructuredLogger.log_event(
            "logout",
            user_id=user.get('sub'),
            email=user.get('email')
        )
    
    # Clear session
    session.clear()
    
    # Redirect to Auth0 logout
    return redirect(
        f"https://{os.getenv('AUTH0_DOMAIN')}/v2/logout?"
        + urlencode({
            "returnTo": url_for('index', _external=True),
            "client_id": os.getenv('AUTH0_CLIENT_ID')
        }, quote_via=quote_plus)
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
