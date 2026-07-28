
import os
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from flask import session, redirect, url_for, request
from dotenv import load_dotenv

load_dotenv()

oauth = OAuth()

auth0 = oauth.register(
    'auth0',
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    api_base_url=f"https://{os.getenv('AUTH0_DOMAIN')}",
    access_token_url=f"https://{os.getenv('AUTH0_DOMAIN')}/oauth/token",
    authorize_url=f"https://{os.getenv('AUTH0_DOMAIN')}/authorize",
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

def init_auth(app):
    oauth.init_app(app)
    return auth0
