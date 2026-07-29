import os
import sys
import logging
from flask import Flask, render_template, redirect, url_for, session, request
from functools import wraps
from urllib.parse import quote_plus, urlencode
from auth import auth0, init_auth

# Configure logging to output to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('AUTH0_SECRET', 'default-secret-key')

# Force HTTPS in production
if os.getenv('WEBSITE_HOSTNAME'):
    class ReverseProxied(object):
        def __init__(self, app):
            self.app = app

        def __call__(self, environ, start_response):
            scheme = environ.get('HTTP_X_FORWARDED_PROTO')
            if scheme:
                environ['wsgi.url_scheme'] = scheme
            return self.app(environ, start_response)

    app.wsgi_app = ReverseProxied(app.wsgi_app)

# Initialize Auth0
init_auth(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            logger.warning("SECURITY_EVENT: Unauthorized access attempt to protected route")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    user = session.get('user')
    if user:
        logger.info(f"SECURITY_EVENT: Page view - user: {user.get('email')}, route: /")
    else:
        logger.info("SECURITY_EVENT: Page view - anonymous user, route: /")
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    logger.info("SECURITY_EVENT: Login attempt")
    return auth0.authorize_redirect(
        redirect_uri=url_for('callback', _external=True)
    )

@app.route('/callback')
def callback():
    try:
        token = auth0.authorize_access_token()
        resp = auth0.get('userinfo', token=token)
        user = resp.json()
        session['user'] = user
        
        logger.info(f"SECURITY_EVENT: Login success - user_id: {user.get('sub')}, email: {user.get('email')}")
        return redirect(url_for('index'))
    except Exception as e:
        logger.error(f"SECURITY_EVENT: Login failure - {str(e)}")
        return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    user = session.get('user')
    logger.info(f"SECURITY_EVENT: Protected access - user: {user.get('email')}, route: /profile")
    return render_template('profile.html', user=user)

@app.route('/protected')
@login_required
def protected():
    user = session.get('user')
    logger.info(f"SECURITY_EVENT: Protected access - user: {user.get('email')}, route: /protected")
    return render_template('protected.html', user=user)

@app.route('/logout')
def logout():
    user = session.get('user')
    if user:
        logger.info(f"SECURITY_EVENT: Logout - user: {user.get('email')}")
    session.clear()
    return redirect(
        f"https://{os.getenv('AUTH0_DOMAIN')}/v2/logout?"
        + urlencode({
            "returnTo": url_for('index', _external=True),
            "client_id": os.getenv('AUTH0_CLIENT_ID')
        }, quote_via=quote_plus)
    )

@app.route('/health')
def health():
    return {"status": "healthy"}, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
