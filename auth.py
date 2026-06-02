import os
from auth0_server_python.auth_server.server_client import ServerClient
from dotenv import load_dotenv

load_dotenv()

class MemoryStateStore:
    def __init__(self):
        self._data = {}
    async def get(self, key, options=None):
        return self._data.get(key)
    async def set(self, key, value, options=None):
        self._data[key] = value
    async def delete(self, key, options=None):
        self._data.pop(key, None)

class MemoryTransactionStore:
    def __init__(self):
        self._data = {}
    async def get(self, key, options=None):
        return self._data.get(key)
    async def set(self, key, value, options=None):
        self._data[key] = value
    async def delete(self, key, options=None):
        self._data.pop(key, None)

state_store = MemoryStateStore()
transaction_store = MemoryTransactionStore()

auth0 = ServerClient(
    domain=os.getenv('AUTH0_DOMAIN'),
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    secret=os.getenv('AUTH0_SECRET'),
    redirect_uri=os.getenv('AUTH0_REDIRECT_URI'),
    state_store=state_store,
    transaction_store=transaction_store,
    authorization_params={
        'scope': 'openid profile email',
        'audience': os.getenv('AUTH0_AUDIENCE', '')
    }
)